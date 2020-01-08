from buildings.models import BuildingFloor, Building
from django.contrib.gis.db import models as gis_models
from django.utils.translation import ugettext as _


class NetworklinesBase(gis_models.Model):
    """
    Routing network lines used in routing services
    """
    INDOORWAY = 0

    STAIRWAY = 1
    ELEVATOR = 2
    RAMP = 3

    OUTDOORWAY = 4
    ESCALATOR = 5
    ZEBRA = 6

    STAIRWAY_NO_CHANGE = 11
    RAMP_NO_CHANGE = 33
    ELEVATOR_NO_CHANGE = 22
    ESCALATOR_NO_CHANGE = 55
    PRIVATE = 90

    UBAHN = 66

    ubahn_karlsplatz_to_atom = """
            Karlsplatz
            Wien
            Zu FußZu Fuß
            ca. 1 Min. , 120 m
            
            Karlsplatz
            
            U-BahnU1Wien Leopoldau
             2 Min. (ohne Zwischenhalt)
            
            Stephansplatz
            U-BahnU3Wien Simmering
             6 Min. (5 Haltestellen)
            
            Schlachthausgasse
            Zu FußZu Fuß
             ca. 10 Min. , 800 m
            
            Atominstitut
            Schüttelstraße 115, 1020 Wien"""

    ubahn_karlsplatz_to_arsenal = """
            Karlsplatz
            Wien
            Zu FußZu Fuß
            ca. 1 Min. , 120 m
            Karlsplatz
            U-BahnU1Wien Alaudagasse
             3 Min. (2 Haltestellen)
            
            Hauptbahnhof
            Zu FußZu Fuß
             ca. 4 Min.
            
            Hauptbahnhof S+U
            Bus69AWien Simmering S+U
             10 Min. (6 Haltestellen)
            
            Lilienthalgasse
            Zu FußZu Fuß
             ca. 4 Min. , 400 m
            
            Franz-Grill-Straße 2-4
            1030 Wien"""

    ROUTE_TYPE = (
        (INDOORWAY, _("Indoor way")),
        (STAIRWAY, _("Stairway")),
        (ELEVATOR, _("Elevator")),
        (ESCALATOR, _("Escalator")),
        (OUTDOORWAY, _("Outdoor way")),
        (RAMP, _("Ramp")),
        (ZEBRA, _("Zebra crossing")),
        (STAIRWAY_NO_CHANGE, _("Stairway no floor change")),
        (RAMP_NO_CHANGE, _("Ramp no floor change")),
        (ELEVATOR_NO_CHANGE, _("Elevator no floor change")),
        (ESCALATOR_NO_CHANGE, _("Escalator no floor change")),
        (PRIVATE, _("Private")),
        )

    ACCESS_TYPE = (
    ("PUBLIC",_("Public")),
    ("PRIVATE",_("Private")),
    ("EMPLOYEE",_("Employee")),
    ("VISITOR",_("Visitor")),
    ("STUDENT",_("Student")),
    ("FACULTY",_("Faculty")),
    ("SECURE",_("Secure")),
    ("RESERVED",_("Reserved")),
    ("MAINTENANCE",_("Maintenance")),
    ("HANDICAP",_("Handicap")),
    ("OTHER",_("Other")),
    ("UNKNOWN",_("Unknown"))
    )

    name = gis_models.CharField(verbose_name=_("short name eg fast networkline"), max_length=150, null=True, blank=True)
    speed = gis_models.DecimalField(verbose_name=_("speed value based on selection"), max_digits=10, decimal_places=2, null=True, blank=True)

    source = gis_models.IntegerField(verbose_name=_("source node id"), null=True, blank=True)
    target = gis_models.IntegerField(verbose_name=_("target node id"), null=True, blank=True)
    cost = gis_models.DecimalField(verbose_name=_("cost to travel network"), max_digits=10, decimal_places=2, null=True, blank=True)
    length = gis_models.DecimalField(verbose_name=_("gis length of linestring"), max_digits=10, decimal_places=2, null=True, blank=True)
    floor_num = gis_models.IntegerField(verbose_name=_("floor number"), null=True, blank=True)

    network_type = gis_models.IntegerField(verbose_name=_("Type of network path type"), choices=ROUTE_TYPE, null=True, blank=True)
    access_type = gis_models.CharField(verbose_name=_("Routing access type"),  max_length=150, choices=ACCESS_TYPE, null=True, blank=True)

    fk_building = gis_models.ForeignKey(Building, on_delete=gis_models.CASCADE, null=True, blank=True)

    geom = gis_models.MultiLineStringField(srid=3857, dim=3, spatial_index=True, null=True, blank=True)


    class Meta:
        abstract = True
        ordering = ['network_type']

    def __str__(self):
        return str(self.name) or ''


class NetworklinesE00(NetworklinesBase):
    """
    Routing network lines used in routing services
    """
    pass


class NetworklinesE01(NetworklinesBase):
    """
    Routing network lines used in routing services
    """
    pass


class NetworklinesE02(NetworklinesBase):
    """
    Routing network lines used in routing services
    """
    pass


class NetworklinesE03(NetworklinesBase):
    """
    Routing network lines used in routing services
    """
    pass
