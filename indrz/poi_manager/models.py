import os

from buildings.models import BuildingFloor, Campus
from django.contrib.gis.db import models as gis_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager


# class BaseLookupDomain(models.Model):
#     code = models.CharField(verbose_name=_("code value"), max_length=150, null=True, blank=True)
#     name = models.CharField(verbose_name=_("name value"), max_length=256, null=True, blank=True)
#
#     class Meta:
#         abstract = True
#         ordering = ['code', ]
#
#     def __str__(self):
#         return str(self.name) or ''


# class TimeStampedModelMixin(models.Model):
#     # Computed values (managed at DB-level with triggers)
#     date_insert = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_(u"Insertion date"),
#                                        db_column='date_insert', null=True, blank=True)
#     date_update = models.DateTimeField(auto_now=True, editable=False, verbose_name=_(u"Update date"),
#                                        db_column='date_update', null=True, blank=True)
#
#     class Meta:
#         abstract = True
#
#     def reload(self, fromdb=None):
#         """Reload fields computed at DB-level (triggers)
#         """
#         if fromdb is None:
#             fromdb = self.__class__.objects.get(pk=self.pk)
#         self.date_insert = fromdb.date_insert
#         self.date_update = fromdb.date_update
#         return self

# Receive the pre_delete signal and delete the file associated with the model instance.

class PoiIcon(models.Model):
    """
    An image added to an icon of the map.
    """
    name = models.CharField(verbose_name=_('Name of map icon'),max_length=255)
    icon = models.ImageField(verbose_name=_('Poi icon image'), upload_to='poi-icons', max_length=512)

    def pictogram_img(self):
        parse_url = self.icon.url
        n_url = parse_url.replace("media/", "")
        print(parse_url)

        return u'<img src="%s" />' % (n_url if self.icon else "")

    pictogram_img.short_description = _("Pictogram")
    pictogram_img.allow_tags = True

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


@receiver(post_delete, sender=PoiIcon)
def poi_icon_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.poi_icon and instance.poi_icon.name:
        if os.path.isfile(instance.poi_icon.path):
            os.remove(instance.poi_icon.path)


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
