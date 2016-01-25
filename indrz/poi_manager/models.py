from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.gis.db import models as gis_model
from buildings.models import Building, BuildingFloor


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


class PoiCategory(MPTTModel):
    cat_name = models.CharField(verbose_name=_('Category name'),max_length=255, null=True, blank=True)
    icon_css_name = models.CharField(verbose_name=_("Icon CSS name"), max_length=255, null=True, blank=True)
    description = models.CharField(verbose_name=_("description"), max_length=255, null=True, blank=True)

    force_mid_point = models.NullBooleanField(verbose_name=_("Force route to this location"), null=True, blank=True)
    enabled = models.NullBooleanField(verbose_name=_("Activated and enabled"), null=True, blank=True)
    tree_order = models.IntegerField(verbose_name=_("Tree order in legend"), null=True, blank=True)
    sort_order = models.IntegerField(verbose_name=_("Sort oder of POI items"), null=True, blank=True)


    tags = TaggableManager(blank=True)
    parent = TreeForeignKey('self',
                        related_name='children',
                        db_index=True,
                        blank=True,
                        null=True,
                            default=9999)

    def __str__(self):
        return str(self.cat_name) or ''




class Poi(models.Model):
    """
     Points of Interest in and around buildings
    """
    name = models.CharField(max_length=255)
    floor_num = models.IntegerField(verbose_name=_("floor number"), null=True, blank=True)

    # icon_class = models.CharField(max_length=255, blank=True, null=True)
    # connect to APP Buildings to enable floors for each POI per level ie floor

    fk_building_floor = models.ForeignKey(BuildingFloor, null=True, blank=True)
    fk_building = models.ForeignKey(Building, null=True, blank=True)

    fk_poi_category = models.ForeignKey(PoiCategory, null=True, blank=True)

    geom = gis_model.MultiPointField(srid=3857, spatial_index=True, db_column='geom', null=True, blank=True)
    objects = gis_model.GeoManager()

    tags = TaggableManager(blank=True)

    def __str__(self):
        return str(self.name) or ''
