from buildings.models import BuildingFloor
from django.contrib.gis.db import models as gis_models
from django.utils.translation import ugettext_lazy as _
from buildings.models import OrganizationInfoBase


class Exhibitor(OrganizationInfoBase):
    """
    Exhibitor information
    """


    pass


class Stands(gis_models.Model):
    """
    Conference Stand locations
    """

    short_name = gis_models.CharField(verbose_name=_(u"short name of stand"), max_length=150, null=True, blank=True)
    long_name = gis_models.CharField(verbose_name=_(u"long stand name"), max_length=150, null=True, blank=True)
    label = gis_models.CharField(verbose_name=_(u"label of stand"), max_length=150, null=True, blank=True)
    foyer_location = gis_models.CharField(verbose_name=_(u"foyer name location value"), max_length=150, null=True, blank=True)
    stand_id_external = gis_models.CharField(verbose_name=_(u"stand id from external system"), max_length=150, null=True, blank=True)
    stand_num_external = gis_models.CharField(verbose_name=_(u"stand number from external"), max_length=150, null=True, blank=True)
    stand_type = gis_models.CharField(verbose_name=_(u"type of stand"), max_length=150, null=True, blank=True)


    fk_building_floor = gis_models.ForeignKey(BuildingFloor)
    fk_exhibitor = gis_models.ForeignKey(Exhibitor)


    multi_polygon = gis_models.MultiPolygonField(srid=3857, spatial_index=True, db_column='geom', null=True, blank=True)
    objects = gis_models.GeoManager()

    class Meta:
        ordering = ['fk_building_floor']

    def __str__(self):
        return str(self.short_name) or u''



