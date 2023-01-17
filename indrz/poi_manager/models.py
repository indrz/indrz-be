import sys
from io import BytesIO

from django.contrib.gis.db import models as gis_model
from django.contrib.postgres.fields import ArrayField
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from PIL import Image as Pilimage

from buildings.models import BuildingFloor, Campus

class PoiIcon(models.Model):
    """
    An image added to an icon of the map.
    """
    name = models.CharField(verbose_name=_('Name of map icon'),max_length=255)
    icon = models.ImageField(verbose_name=_('Poi icon image'), upload_to='poi_icons',
                             max_length=512, default="/poi_icons/other_pin.png")

    class Meta:
        ordering = ('name', )

    @property
    def json(self):
        return {
            "id": self.pk,
            "name": self.name,
            "src": self.icon.url
        }

    def __str__(self):
        return self.name


class PoiCategory(MPTTModel):
    cat_name = models.CharField(verbose_name=_('Category name'),max_length=255, null=True, blank=True)
    icon_css_name = models.CharField(verbose_name=_("Icon CSS name"), max_length=255, null=True, blank=True)
    fk_poi_icon = models.ForeignKey(PoiIcon, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(verbose_name=_("description"), max_length=255, null=True, blank=True)

    force_mid_point = models.BooleanField(verbose_name=_("Force route to this location"), null=True, blank=True)
    enabled = models.BooleanField(verbose_name=_("Activated and enabled"), null=True, blank=True)
    tree_order = models.IntegerField(verbose_name=_("Tree order in legend"), null=True, blank=True)
    sort_order = models.IntegerField(verbose_name=_("Sort oder of POI items"), null=True, blank=True)

    tags = TaggableManager(blank=True)
    parent = TreeForeignKey('self',
                        related_name='children', on_delete = models.CASCADE,
                        db_index=True,
                        blank=True,
                        null=True,
                            default=9999)
    cat_name_en = models.CharField(max_length=255, null=True, blank=True)
    cat_name_de = models.CharField(max_length=255, null=True, blank=True)

    html_content = models.TextField(_("HTML content"), null=True, blank=True)

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
        return str(self.name) or ''


class PoiImages(models.Model):
    poi = models.ForeignKey(Poi, on_delete=models.CASCADE)
    images = models.ImageField(verbose_name=_('POI images'), upload_to='poi_images', max_length=512)
    thumbnails = models.ImageField(verbose_name=_('POI Image Thumbnail'), upload_to='poi_thumbnails',
                                   null=True, blank=True, max_length=512)

    def save(self, *args, **kwargs):

        img = Pilimage.open(self.images)

        if img.height > 400 or img.width > 400:

            desired_size = (408, 250)
            thumbnail_bytes = BytesIO()

            ##############  self crop   ###########################

            im_size = img.size
            new_size = img.size

            if im_size[0] >= im_size[1]:
                # Check if the image is already the desired size
                if im_size[1] > desired_size[1]:
                    x_axis = int(desired_size[1] / im_size[1] * im_size[0])
                    y_axis = desired_size[1]
            elif im_size[1] > im_size[0]:
                # Check if the image is already the desired size
                if im_size[0] > desired_size[0]:
                    x_axis = desired_size[0]
                    y_axis = int(desired_size[0] / im_size[0] * im_size[1])
            new_size = (x_axis, y_axis)

            im_resized = img.resize(new_size)

            # Find the center of the image
            left = int(im_resized.size[0] / 2 - desired_size[0] / 2)
            upper = int(im_resized.size[1] / 2 - desired_size[1] / 2)
            right = left + desired_size[0]
            lower = upper + desired_size[1]

            # Crop and save the image
            im_cropped = im_resized.crop((left, upper, right, lower))

            im_cropped.save(
                thumbnail_bytes, "jpeg", quality=60, optimize=True, progressive=True
            )

            img_name = self.images.name.split('.')[0]

            # good for simple thumbnails but not good for portrait size images ie height > width
            # img.thumbnail(desired_size, Pilimage.ANTIALIAS)

            img.save(
                thumbnail_bytes, "jpeg", quality=60, optimize=True, progressive=True
            )
            self.thumbnails = InMemoryUploadedFile(thumbnail_bytes, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg',
                                                   sys.getsizeof(thumbnail_bytes), None)

        force_update = False

        # If the instance already has been saved, it has an id and we set
        # force_update to True
        if self.id:
            force_update = True

        # Force an UPDATE SQL query if we're editing the image to avoid integrity exception
        super(PoiImages, self).save(force_update=force_update)

    def __str__(self):
        return self.images.name or ''