import json

from django.contrib.gis.gdal.geometries import OGRGeometry
from django.db import models
from django.utils.translation import gettext_lazy as _

from organizations.models import Organization


# Create your models here.
class Campus(models.Model):
    """
    A campus is  location of one or more buildings that belong together somehow
    how is determined by the organization.
    """

    name = models.CharField(verbose_name=_("Campus name"), max_length=128)
    description = models.CharField(verbose_name=_("Building description"), max_length=256, null=True, blank=True)

    fk_organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    geom = models.MultiPolygonField(verbose_name=_("Campus area of one or more buildings"),
                                                 blank=True, null=True, srid=3857, spatial_index=True)

    sort_order = models.IntegerField(verbose_name=_('Display order'), null=True, blank=True)

    @property
    def centroid(self):
        #TODO this is a hack work around
        # code should simply be one liner but it returns ogr error no idea why ! it works in django 1.11
        # json.loads(self.geom.centroid.json)
        g = OGRGeometry(self.geom.centroid.wkt)
        return json.loads(g.json)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return str(self.name) or ''