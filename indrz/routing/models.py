from buildings.models import BuildingFloor, Building
from django.contrib.gis.db import models as gis_models
from django.utils.translation import ugettext_lazy as _


class LtNetworkTypeDomain(gis_models.Model):
    """
    Look up table with the different types of network lines
    """
    code = gis_models.CharField(verbose_name=_(u"type code value"), max_length=150, null=True, blank=True)
    type_name = gis_models.CharField(verbose_name=_(u"Network line type name"), max_length=256, null=True, blank=True)


    def __str__(self):
        return str(self.name) or u''

class Networklines(gis_models.Model):
    """
    Routing network lines used in routing services
    """

    short_name = gis_models.CharField(verbose_name=_(u"short name eg fast networkline"), max_length=150, null=True, blank=True)
    speed = gis_models.DecimalField(verbose_name=_(u"speed value based on selection"), max_digits=10, decimal_places=2, null=True, blank=True)

    source = gis_models.IntegerField(verbose_name=_(u"source node id"), null=True, blank=True, db_column='source')
    target = gis_models.IntegerField(verbose_name=_(u"target node id"), null=True, blank=True, db_column='target')
    cost = gis_models.DecimalField(verbose_name=_(u"cost to travel network"), max_digits=10, decimal_places=2, null=True, blank=True)
    length = gis_models.DecimalField(verbose_name=_(u"gis length of linestring"), max_digits=10, decimal_places=2, null=True, blank=True)


    fk_building_floor = gis_models.ForeignKey(BuildingFloor)
    fk_lt_network_type = gis_models.ForeignKey(LtNetworkTypeDomain, null=True, blank=True)

    multi_linestring = gis_models.MultiLineStringField(srid=3857, spatial_index=True, db_column='geom', null=True, blank=True)
    objects = gis_models.GeoManager()

    class Meta:
        ordering = ['fk_building_floor']

    def __str__(self):
        return str(self.short_name) or u''




