from django.contrib.gis.db import models

# Create your models here.

class NamedModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Zoneplan(NamedModel):
    name = models.CharField(max_length=100)
    mainuse = models.CharField(max_length=100)
    orgcode = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    room_code = models.CharField(max_length=100)
    floor = models.CharField(max_length=100)
    org_color = models.CharField(max_length=100)
    mainuse_color = models.CharField(max_length=100)
    surface_type_id = models.CharField(max_length=100)
    secondary_users = models.CharField(max_length=100)
    geom = models.PolygonField( db_column='geom', blank=True, null=True, srid=3857, spatial_index=True)


    def __str__(self):
        return self.name





