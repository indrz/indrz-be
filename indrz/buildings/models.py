from __future__ import unicode_literals

import json

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.gdal import OGRGeometry
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _


class BaseLookupDomain(gis_models.Model):
    code = gis_models.CharField(verbose_name=_("code value"), max_length=150, null=True, blank=True)
    name = gis_models.CharField(verbose_name=_("name value"), max_length=256, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['code',]

    def __str__(self):
        return str(self.name) or ''


class LtAccessType(BaseLookupDomain):
    # translate LT values in the databse project
    # https://github.com/ecometrica/django-vinaigrette

    # ACCESS_TYPE = (
    # ('PUBLIC',_('Public')),
    # ('PRIVATE',_('Private')),
    # ('EMPLOYEE',_('Employee')),
    # ('VISITOR',_('Visitor')),
    # ('STUDENT',_('Student')),
    # ('FACULTY',_('Faculty')),
    # ('SECURE',('Secure')),
    # ('RESERVED',('Reserved')),
    # ('MAINTENANCE',_('Maintenance')),
    # ('HANDICAP',_('Handicap')),
    # ('OTHER',_('Other')),
    # ('UNKNOWN',_('Unknown'))
    # )
    pass

class LtCondition(BaseLookupDomain):
    pass
# Excellent	Excellent
# Very Good	Very Good
# Good	Good
# Fair	Fair
# Poor	Poor
# Very Poor	Very Poor
# Unknown

class LtPlanLineType(BaseLookupDomain):

    # PLAN_LINE_TYPE = (
    #     ('WALLS', _('Walls')),
    #     ('DOORS', _('Doors')),
    #     ('WINDOWS', _('Windows')),
    #     ('ARROWS', _('Arrows')),
    #     ('RAMPS', _('Ramps')),
    #     ('STAIRS', _('Stairs')),
    #     ('ELEVATOR', _('Elevator')),
    #     ('ESCALATOR', _('Escalator')),
    #     ('FURNITURE', _('Furniture')),
    #     ('BATHROOM', _('Bathroom')),
    #     ('GLASS', _('Glass')),
    #     )
    #
# Cased Opening	Cased Opening
# Chainlink Cage	Chainlink Cage
# Column	Column
# Door	Door
# Exterior Wall	Exterior Wall
# Glass Wall	Glass Wall
# Inferred Line	Inferred Line
# Interior Wall	Interior Wall
# Movable Wall	Movable Wall
# Partial Height Wall	Partial Height Wall
# Phantom Line	Phantom Line
# Sloping Wall	Sloping Wall
# Stair	Stair
# Stair Other Floor	Stair Other Floor
# Window Frame	Window Frame
# Window Pane	Window Pane
# Other	Other
# Unknown	Unknown
    pass


class LtSpaceType(BaseLookupDomain):
    # SPACE_TYPE = (
    #     ('OFFICE', _('Office')),
    #     ('HALLWAY', _('Hallway')),
    #     ('STAIRWAY', _('Stairway')),
    #     ('ELEVATOR', _('Elevator')),
    #     ('ESCALATOR', _('Escalator')),
    #     ('FOYER', _('Foyer')),
    #     ('LOBBY', _('Lobby')),
    #     ('INFORMATION', _('Information')),
    #      ('CAFETERIA', _('Cafeteria')),
    #     ('LOUNGE', _('Lounge')),
    #     ('WC', _('Bathroom')),
    #     ('SHOWER', _('Shower')),
    #     ('CHANGING_ROOM', _('Changing room')),
    #     ('PROJECT_ROOM', _('Project room')),
    #     ('MEETING_ROOM', _('Meeting room')),
    #     ('STUDY_ROOM', _('Study room')),
    #     ('CONFERENCE_ROOM', _('Conference room')),
    #     ('COMMON_ROOM', _('Common room')),
    #     ('PATIO', _('Terrace patio')),
    #     ('ROOM UNKNOWN', _('Room unknown')),
    #     )
    pass


class BuildingAddressBase(gis_models.Model):
    """
    physical base address information of a building
    """
    street = gis_models.CharField(verbose_name=_("Street"), max_length=256,
                              blank=True, null=True)
    house_number = gis_models.CharField(verbose_name=_("Building or house number"), max_length=10,
                              blank=True, null=True)
    postal_code = gis_models.CharField(verbose_name=_("Postal code"), max_length=8,
                                   blank=True, null=True)
    municipality = gis_models.CharField(verbose_name=_("Municipality"),
                                    blank=True, null=True,
                                    max_length=256)
    city = gis_models.CharField(verbose_name=_("City"),
                                    blank=True, null=True,
                                    max_length=256)

    country = gis_models.CharField(verbose_name=_("Country"),
                                    blank=True, null=True,
                                    max_length=256)
    class Meta:
        abstract = True
        ordering = ['city']

    def __str__(self):
        return str(self.city) or ''


class OrganizationInfoBase(BuildingAddressBase):
    name = gis_models.CharField(verbose_name=_("Name"), max_length=256, null=True, blank=True)
    description = gis_models.TextField(verbose_name=_("Description"),
                                   help_text=_("Brief description"), null=True, blank=True)
    phone = gis_models.CharField(verbose_name=_("Phone"), max_length=32,
                             blank=True, null=True)
    email = gis_models.EmailField(verbose_name=_("Email"), max_length=256,
                              blank=True, null=True)
    website = gis_models.URLField(verbose_name=_("Website"), max_length=256, blank=True, null=True)
    # photo = gis_models.FileField(verbose_name=_(u"Photo"), upload_to=settings.UPLOAD_DIR,
    #                          db_column='photo', max_length=512, blank=True, null=True)

    geom = gis_models.PointField(verbose_name=_("Building centroid for small scale maps"),
                             blank=True, null=True, srid=3857, spatial_index=False)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return str(self.name) or ''


class Organization(OrganizationInfoBase):
    """
    Represents a customer or Uni that has one or more building locations

    """
    owner = gis_models.CharField(verbose_name=_("Owner name"), max_length=128, null=True, blank=True)
    legal_form = gis_models.CharField(verbose_name=_("Legal entity form"), max_length=128, null=True, blank=True)
    num_buildings = gis_models.IntegerField(verbose_name=_("Number of buildings"), null=True, blank=True)



class Campus(gis_models.Model):
    """
    A campus is  location of one or more buildings that belong together somehow
    how is determined by the organization.
    """

    campus_name = gis_models.CharField(verbose_name=_("Campus name"), max_length=128, null=True, blank=True)
    description = gis_models.CharField(verbose_name=_("Building description"), max_length=256, null=True, blank=True)

    fk_organization = gis_models.ForeignKey(Organization, on_delete=gis_models.CASCADE)

    geom = gis_models.MultiPolygonField(verbose_name=_("Campus area of one or more buildings"),
                                                 blank=True, null=True, srid=3857, spatial_index=True)

    sort_order = gis_models.IntegerField(verbose_name=_('Display order'), null=True, blank=True)

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
        return str(self.campus_name) or ''


class Building(OrganizationInfoBase):
    """
    A physical building that only has one address
    """

    building_name = gis_models.CharField(verbose_name=_("Building name"), max_length=128, null=True, blank=True)
    building_height = gis_models.DecimalField(verbose_name=_("Building height in meters"), max_digits=10, decimal_places=2, null=True, blank=True)
    fancy_name = gis_models.CharField(verbose_name=_("Fancy building name"), max_length=256, null=True, blank=True)
    num_floors = gis_models.IntegerField(verbose_name=_("Number of floors"), default=0)
    facility_number = gis_models.IntegerField(verbose_name=_("Unique facility number"), null=True, blank=True)
    operation_hrs = gis_models.CharField(verbose_name=_("Operational hours"), max_length=60, null=True, blank=True)
    native_epsg = gis_models.IntegerField(verbose_name=_("EPSG code original data"), null=True, blank=True)
    detail_description = gis_models.CharField(verbose_name=_("Building description"), max_length=256, null=True, blank=True)
    wings = gis_models.CharField(verbose_name=_('Wing'), max_length=800, null=True, blank=True)

    fk_organization = gis_models.ForeignKey(Organization, on_delete=gis_models.CASCADE)
    fk_campus = gis_models.ForeignKey(Campus, null=True, blank=True, related_name='buildings', on_delete=gis_models.CASCADE)


class BuildingFloor(gis_models.Model):
    """
    A floor representing a single building floor
    """
    short_name = gis_models.CharField(verbose_name=_("short name eg first floor"), max_length=150, null=True, blank=True)
    long_name = gis_models.CharField(verbose_name=_("long name"), max_length=150, null=True, blank=True)
    special_name = gis_models.CharField(verbose_name=_("special name"), max_length=150, null=True, blank=True)

    vertical_order = gis_models.IntegerField(verbose_name=_("Floor order value"), null=True, blank=True)
    base_elevation = gis_models.IntegerField(verbose_name=_("Elevation value of floor in meters"), null=True, blank=True)

    floor_num = gis_models.FloatField(verbose_name=_("floor number"),null=True, blank=True)
    floor_name = gis_models.CharField(verbose_name=_("floor name"), max_length=200,null=True, blank=True)
    floor_height = gis_models.DecimalField(verbose_name=_("height of floor"), max_digits=5, decimal_places=2, null=True, blank=True)


    fk_building = gis_models.ForeignKey(Building, on_delete=gis_models.CASCADE)

    geom = gis_models.MultiPolygonField(srid=3857, spatial_index=True, null=True, blank=True)

    tags = ArrayField(ArrayField(gis_models.CharField(max_length=255),
                                 blank=True, null=True), null=True, blank=True)


    class Meta:
        ordering = ['floor_num']

    def __str__(self):
        return self.short_name + " (" + self.fk_building.name + " )" or ''


class FloorSpaceBase(gis_models.Model):
    """
    Base class for modeling any polygons.
    """

    short_name = gis_models.CharField(verbose_name=_("short name"), max_length=150, null=True, blank=True)
    long_name = gis_models.CharField(verbose_name=_("long name"), max_length=150, null=True, blank=True)
    area = gis_models.DecimalField(verbose_name=_("gis calculated area"), max_digits=10, decimal_places=2, null=True, blank=True)
    perimeter = gis_models.DecimalField(verbose_name=_("gis calculated perimeter"), max_digits=10, decimal_places=2, null=True, blank=True)
    floor_num = gis_models.FloatField(verbose_name=_("floor number"),null=True, blank=True)
    floor_name = gis_models.CharField(verbose_name=_("floor name"), max_length=200,null=True, blank=True)
    geom = gis_models.MultiPolygonField(srid=3857, spatial_index=True, null=True, blank=True)

    fk_access_type = gis_models.ForeignKey(LtAccessType, null=True, blank=True, on_delete=gis_models.CASCADE)
    fk_building_floor = gis_models.ForeignKey(BuildingFloor, on_delete=gis_models.CASCADE)
    fk_building = gis_models.ForeignKey(Building, on_delete=gis_models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.short_name or ''


class BuildingFloorPlanLine(gis_models.Model):
    """
    Represents the lines that compose a floor plan, such as walls, doors, and windows.
    """


    # line_type = gis_models.CharField(verbose_name=_(u"Cartography line type"), max_length=150, null=True,
    #                               blank=True, choices=PLAN_LINE_TYPE)

    short_name = gis_models.CharField(verbose_name=_("short name"), max_length=150, null=True, blank=True)
    long_name = gis_models.CharField(verbose_name=_("long name"), max_length=150, null=True, blank=True)
    # floor_number = gis_models.IntegerField(verbose_name=_(u"floor number"),null=True, blank=True)
    length = gis_models.DecimalField(verbose_name=_("gis calculated length"), max_digits=10, decimal_places=2, null=True, blank=True)
    floor_num = gis_models.FloatField(verbose_name=_("floor number"),null=True, blank=True)
    floor_name = gis_models.CharField(verbose_name=_("floor name"), max_length=200,null=True, blank=True)

    fk_line_type = gis_models.ForeignKey(LtPlanLineType, on_delete=gis_models.CASCADE, null=True, blank=True)
    fk_building_floor = gis_models.ForeignKey(BuildingFloor, on_delete=gis_models.CASCADE, null=True, blank=True)

    geom = gis_models.MultiLineStringField(srid=3857, spatial_index=True, null=True, blank=True)

    tags = ArrayField(ArrayField(gis_models.CharField(max_length=150), blank=True, null=True), null=True, blank=True)

    class meta:
        ordering = ['short_name']

    def __str__(self):
        return str(self.short_name) or ''


class InteriorFloorSection(FloorSpaceBase):
    """
    Represents a logical or physical division of a single floor.
    One or more floor sections define a wing, zone, etc.
    """
    organization = gis_models.CharField(verbose_name=_("Organization name e.g Engineering"), max_length=256, null=True, blank=True)
    department = gis_models.CharField(verbose_name=_("Department name e.g Engineering"), max_length=256, null=True, blank=True)
    division = gis_models.CharField(verbose_name=_("Division"), max_length=256, null=True, blank=True)
    tags = ArrayField(ArrayField(gis_models.CharField(max_length=255), blank=True, null=True), null=True, blank=True)
    rule_nearest_entrance = gis_models.ManyToManyField('poi_manager.Poi',
                                                       limit_choices_to={'category': 13}, blank=True)

class BuildingFloorSpace(FloorSpaceBase):
    """
     an interior space such as hallways, rooms, and stairwells.
    """

    room_external_id = gis_models.CharField(verbose_name=_("Room id imported from external system"), max_length=150, null=True, blank=True)
    room_number = gis_models.CharField(verbose_name=_("Room number"), max_length=150, null=True, blank=True)
    room_number_sign = gis_models.CharField(verbose_name=_("Room number on door sign"), max_length=150, null=True, blank=True)
    room_description = gis_models.CharField(verbose_name=_("Room description"), max_length=150, null=True, blank=True)
    room_code = gis_models.CharField(verbose_name=_("Room code"), max_length=150, null=True, blank=True)
    capacity = gis_models.IntegerField(verbose_name=_("Total number of occupants allowed in this space"), null=True, blank=True)

    space_type = gis_models.ForeignKey(LtSpaceType, on_delete=gis_models.CASCADE, null=True, blank=True)

    tag = gis_models.TextField(verbose_name=_("Tag values csv"), null=True, blank=True)
    tags = ArrayField(ArrayField(gis_models.CharField(max_length=150), blank=True, null=True), null=True, blank=True)


    @property
    def centerGeometry(self):
        return self.geom.centroid

    class Meta:
        ordering = ['room_code']


class Wing(FloorSpaceBase):
    """
    Represents a logical or physical division of a single floor.
    One or more floor sections define a wing, zone, etc.
    """
    name = gis_models.CharField(verbose_name=_("Wing name"), max_length=256, null=True, blank=True)
    abbreviation = gis_models.CharField(verbose_name=_("Abbreviation"), max_length=20, null=True, blank=True)

    def __str__(self):
        return self.abbreviation or ''
