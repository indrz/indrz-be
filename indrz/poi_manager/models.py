import os
from io import BytesIO
from pathlib import Path

from PIL import Image as Pilimage
from django.contrib.gis.db import models as gis_model
from django.contrib.postgres.fields import ArrayField
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import pre_delete, post_delete, pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager

from buildings.models import BuildingFloor, Campus


class PoiIcon(models.Model):
    """
    An image added to an icon of the map.
    """
    name = models.CharField(verbose_name=_('Name of map icon'), max_length=255)
    icon = models.ImageField(verbose_name=_('Poi icon image'), upload_to='poi_icons',
                             max_length=512, default="/poi_icons/other_pin.png")

    class Meta:
        ordering = ('name',)

    @property
    def json(self):
        return {
            "id": self.pk,
            "name": self.name,
            "src": self.icon.url
        }

    def __str__(self):
        return self.name or ''


class PoiCategory(MPTTModel):
    cat_name = models.CharField(verbose_name=_('Category name'), max_length=255, null=True, blank=True)
    icon_css_name = models.CharField(verbose_name=_("Icon CSS name"), max_length=255, null=True, blank=True)
    fk_poi_icon = models.ForeignKey(PoiIcon, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(verbose_name=_("description"), max_length=255, null=True, blank=True)

    force_mid_point = models.BooleanField(verbose_name=_("Force route to this location"), null=True, blank=True)
    enabled = models.BooleanField(verbose_name=_("Activated and enabled"), null=True, blank=True)
    tree_order = models.IntegerField(verbose_name=_("Tree order in legend"), null=True, blank=True)
    sort_order = models.IntegerField(verbose_name=_("Sort oder of POI items"), null=True, blank=True)

    tags = TaggableManager(blank=True)
    parent = TreeForeignKey('self',
                            related_name='children', on_delete=models.CASCADE,
                            db_index=True,
                            blank=True,
                            null=True,
                            default=9999)
    cat_name_en = models.CharField(max_length=255, null=True, blank=True)
    cat_name_de = models.CharField(max_length=255, null=True, blank=True)

    html_content = models.TextField(_("HTML content"), null=True, blank=True)
    html_content_de = models.TextField(_("DE HTML content"), null=True, blank=True)

    def __str__(self):
        return str(self.cat_name) or ''

    @property
    def icon(self):
        if self.fk_poi_icon:
            if self.fk_poi_icon.icon:
                return self.fk_poi_icon.icon.url
            else:
                return ""
        else:
            return ""


class Poi(models.Model):
    """
     Points of Interest in and around buildings
    """
    name = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    name_de = models.CharField(max_length=255, null=True, blank=True)
    floor_num = models.FloatField(verbose_name=_("floor number"), null=True, blank=True)
    floor_name = models.CharField(verbose_name=_("floor name"), max_length=200, null=True, blank=True)
    description = models.CharField(verbose_name=_("description"), max_length=255, null=True, blank=True)
    enabled = models.BooleanField(verbose_name=_("Activated and enabled"), null=True, blank=True)

    floor = models.ForeignKey(BuildingFloor, on_delete=models.DO_NOTHING, null=True, blank=True)
    campus = models.ForeignKey(Campus, on_delete=models.DO_NOTHING, null=True, blank=True)
    category = models.ForeignKey(PoiCategory, on_delete=models.CASCADE)

    geom = gis_model.MultiPointField(srid=3857, spatial_index=True, db_column='geom', null=True, blank=True)

    poi_tags = ArrayField(models.CharField(max_length=50, blank=True), blank=True, null=True)

    html_content = models.TextField(_("HTML content"), null=True, blank=True)
    html_content_de = models.TextField(_("DE HTML content"), null=True, blank=True)

    @property
    def icon(self):
        if self.category.fk_poi_icon:
            if self.category.fk_poi_icon.icon:
                return self.category.fk_poi_icon.icon.url
            else:
                return ""
        else:
            return ""

    def __str__(self):
        if self.name and self.category.cat_name:
            return self.name + ' ( ' + self.category.cat_name + ')'
        else:
            return self.category.cat_name or ''


class PoiImages(models.Model):
    poi = models.ForeignKey(Poi, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_('POI images'), upload_to='poi_images', max_length=512)
    thumbnail = models.ImageField(verbose_name=_('POI Image Thumbnail'), upload_to='poi_images',
                                  null=True, blank=True, max_length=512, editable=False)
    sort_order = models.PositiveSmallIntegerField(verbose_name=_("Order of images"), null=True, blank=True)
    alt_text = models.CharField(verbose_name=_("Html image alt text"), max_length=255, default="Image of ...")

    is_default = models.BooleanField(default=False)

    def set_default(self):
        PoiImages.objects.exclude(id=self.id).update(is_default=False)
        self.is_default = True
        self.save()

    def save(self, *args, **kwargs):
        # If the PoiImage already exists, just save it without modifying the thumbnail or resizing
        if self.pk:
            super().save(*args, **kwargs)
            return

        # Call super save to store changes
        super().save(*args, **kwargs)

        # First handle image resizing
        img = Pilimage.open(self.image)

        # Check if the image needs to be resized
        if img.width > 1980 or img.height > 1980:
            # Calculate aspect ratio
            aspect_ratio = float(img.height) / float(img.width)

            # Resize while maintaining aspect ratio
            if img.height > img.width:
                new_height = 1980
                new_width = int(new_height / aspect_ratio)
            else:
                new_width = 1980
                new_height = int(new_width * aspect_ratio)

            img = img.resize((new_width, new_height), Pilimage.ANTIALIAS)
            img.save(self.image.path)

        # Create thumbnail
        img.thumbnail((400, 250), Pilimage.ANTIALIAS)

        temp_thumb = BytesIO()
        img.save(temp_thumb, format='JPEG')
        temp_thumb.seek(0)

        file_name = Path(self.image.name).stem  # Name without extension
        file_suffix = Path(self.image.name).suffix
        thumb_filename = f"{file_name}_thumbnail{file_suffix}"

        # This saves the thumbnail
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)

        # Call super save to store changes
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        if self.image.name:
            return self.image.name
        else:
            return ''


@receiver(post_delete, sender=PoiImages)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if Path(instance.image.path).is_file():
            os.remove(instance.image.path)

    if instance.thumbnail:
        if Path(instance.thumbnail.path).is_file():
            os.remove(instance.thumbnail.path)


@receiver(pre_save, sender=PoiImages)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False


@receiver(post_save, sender=PoiImages)
def set_all_images_to_not_default_on_default_change(sender, instance, **kwargs):
    """
    Set all other images to not default when one image is set to default
    """
    if instance.is_default == True:
        id = instance.id
        other_images = PoiImages.objects.exclude(id=id)
        for image in other_images:
            image.is_default = False
            image.save()


@receiver(pre_delete, sender=Poi)
def delete_related_images(sender, instance, **kwargs):
    # Delete all related PoiImages before the Poi object is deleted
    instance.poiimages_set.all().delete()
