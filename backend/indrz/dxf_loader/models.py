from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models as gis_model
from buildings.models import Building
from django.contrib.postgres.fields import ArrayField

class DxfLayer(models.Model):
    """
    DxfLayer model corresponds to geodata.dxf_layer table
    Stores information about DXF layers
    """
    names = ArrayField(
        models.TextField(),
        null=False,
        blank=False,
        default=list,
        help_text=_('List of layer names')
    )

    class LayerType(models.TextChoices):
        SPACES = 'spaces', _('Spaces')
        UNIQUEID = 'uniqueid', _('Unique ID')
        DOORS = 'doors', _('Doors')
        STAIRS = 'stairs', _('Stairs')
        ELEVATOR = 'elevator', _('Elevator')
        RAMP = 'ramp', _('Ramp')
        INNERWALL = 'innerwall', _('Inner Wall')
        OUTERWALL = 'outerwall', _('Outer Wall')
        FURNITURE = 'furniture', _('Furniture')

    type = models.CharField(
        max_length=16,
        choices=LayerType.choices,
        default=LayerType.FURNITURE,
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    FileRegistry = models.ForeignKey(
        'FileRegistry',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='dxf_layers'
    )

    class Meta:
        verbose_name = _('DXF Layer')
        verbose_name_plural = _('DXF Layers')

    def __str__(self):
        return str(self.names)


class FileRegistry(models.Model):
    """
    FileRegistry model corresponds to geodata.file_registry table
    Stores information about DXF files that have been loaded into the system
    """
    path = models.TextField(null=False, blank=False, unique=True)
    table_raw = models.TextField(null=False, blank=False)
    mtime = models.DateTimeField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    building_code = models.TextField(null=True, blank=True)
    floor_name = models.TextField(null=True, blank=True)
    floor_number = models.FloatField(null=True, blank=True)

    building = models.ForeignKey(
        Building,  
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='file_registry'
    )

    class Meta:
        verbose_name = _('File Registry')
        verbose_name_plural = _('File Registries')

    def __str__(self):
        return self.path


class GeorefParams(models.Model):
    """
    GeorefParams model corresponds to geodata.georef_params table
    Stores georeferencing parameters for DXF files
    """
    table_raw = models.TextField(null=False, blank=False)
    x_org = models.FloatField(null=True, blank=True)
    y_org = models.FloatField(null=True, blank=True)
    x_geo = models.FloatField(null=True, blank=True)
    y_geo = models.FloatField(null=True, blank=True)
    scale = models.FloatField(default=1.0)
    rotate = models.FloatField(default=0.0, help_text=_('degrees'))
    updated_at = models.DateTimeField(auto_now=True)
    geom_georef = gis_model.PointField(
        srid=3857,
        spatial_index=True,
        db_column='geom',
        null=True,
        blank=True
    )
    FileRegistry = models.ForeignKey(
        FileRegistry,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='georef_params'
    )

    class Meta:
        verbose_name = _('Georeferencing Parameter')
        verbose_name_plural = _('Georeferencing Parameters')

    def __str__(self):
        return self.table_raw


class DxfImportedTable(models.Model):
    """
    DxfImportedTable model stores information about raw data tables created
    when a DXF file is imported using ogr2ogr
    """
    table_name = models.TextField(null=False, blank=False)
    schema_name = models.TextField(default='dxf_raw')
    import_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    srid = models.IntegerField(null=True, blank=True)
    has_georef = models.BooleanField(default=False, help_text=_('Indicates if this raw table has been georeferenced'))

    # Foreign key to FileRegistry
    file_registry = models.ForeignKey(
        FileRegistry,
        on_delete=models.CASCADE,
        related_name='imported_tables'
    )

    # If the table has been georeferenced, store the reference to the georeferenced table
    georef_table_name = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _('DXF Imported Table')
        verbose_name_plural = _('DXF Imported Tables')

    def __str__(self):
        return f"{self.schema_name}.{self.table_name}"

    @property
    def full_table_name(self):
        """
        Returns the fully qualified table name (schema.table)
        """
        return f"{self.schema_name}.{self.table_name}"


# class DxfGeometryData(gis_model.Model):
#     """
#     Base abstract model representing the table structure created by ogr2ogr when importing DXF files.

#     This model maps to the tables that ogr2ogr creates when importing DXF files.
#     Each imported DXF file creates a new table with this structure.
#     """
#     ogc_fid = models.AutoField(primary_key=True)
#     layer = models.CharField(max_length=255, null=True, blank=True)
#     paperspace = models.BooleanField(null=True, blank=True)
#     subclasses = models.CharField(max_length=255, null=True, blank=True)
#     linetype = models.CharField(max_length=255, null=True, blank=True)
#     entityhandle = models.CharField(max_length=255, null=True, blank=True)
#     text = models.CharField(max_length=255, null=True, blank=True)
#     # Using GeometryField to support any geometry type (point, line, polygon)
#     # The field name is wkb_geometry in the database, but we'll use 'geom' in Django
#     geom = gis_model.GeometryField(srid=31259, spatial_index=True, db_column='wkb_geometry')

#     imported_table = models.ForeignKey(
#         DxfImportedTable,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name='geometry_data'
#     )

#     class Meta:
#         abstract = True
#         verbose_name = _('DXF Geometry Data')
#         verbose_name_plural = _('DXF Geometry Data')

#     def __str__(self):
#         return f"{self.layer} - {self.entityhandle or 'No handle'}"


# class DxfRawData(DxfGeometryData):
#     """
#     Model for raw DXF data imported by ogr2ogr.
#     This model is used to represent the raw imported data before georeferencing.
#     """
#     class Meta:
#         verbose_name = _('DXF Raw Data')
#         verbose_name_plural = _('DXF Raw Data')
#         # This is a proxy model - it doesn't create its own table
#         # Instead, it uses Django's dynamic model creation to map to the actual tables
#         managed = False


# class DxfGeoData(DxfGeometryData):
#     """
#     Model for georeferenced DXF data.
#     This model is used to represent the georeferenced data after transformation.
#     """
#     class Meta:
#         verbose_name = _('DXF Georeferenced Data')
#         verbose_name_plural = _('DXF Georeferenced Data')
#         # This is a proxy model - it doesn't create its own table
#         managed = False