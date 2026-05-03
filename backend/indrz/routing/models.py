from buildings.models import BuildingFloor, Building
from django.contrib.gis.db import models as gis_models
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.db import models


class RoutingEdge(gis_models.Model):
    """
    A single routing segment (edge) used by the indoor routing engine.
    """

    LINE_TYPE_INDOOR = "indoor"
    LINE_TYPE_OUTDOOR = "outdoor"
    LINE_TYPE_ELEVATOR = "elevator"
    LINE_TYPE_ELEVATOR_NO_FLOOR_CHANGE = "elevator-no-floor-change"
    LINE_TYPE_STAIRS = "stairs"
    LINE_TYPE_STAIRS_NO_FLOOR_CHANGE = "stairs-no-floor-change"
    LINE_TYPE_RAMPS = "ramps"

    LINE_TYPE_CHOICES = [
        (LINE_TYPE_INDOOR, "Indoor"),
        (LINE_TYPE_OUTDOOR, "Outdoor"),
        (LINE_TYPE_ELEVATOR, "Elevator"),
        (LINE_TYPE_ELEVATOR_NO_FLOOR_CHANGE, "Elevator (no floor change)"),
        (LINE_TYPE_STAIRS, "Stairs"),
        (LINE_TYPE_STAIRS_NO_FLOOR_CHANGE, "Stairs (no floor change)"),
        (LINE_TYPE_RAMPS, "Ramps"),
    ]

    SRID = 3857  # adapt to your project SRID if needed

    geom = gis_models.LineStringField(srid=SRID)

    campus = models.ForeignKey(
        "campus.Campus",
        on_delete=models.CASCADE,
        related_name="routing_edges",
    )
    building = models.ForeignKey(
        "buildings.Building",
        on_delete=models.CASCADE,
        related_name="routing_edges",
    )
    floor_from = models.ForeignKey(
        "buildings.BuildingFloor",
        on_delete=models.CASCADE,
        related_name="routing_edges_from",
    )
    floor_to = models.ForeignKey(
        "buildings.BuildingFloor",
        on_delete=models.CASCADE,
        related_name="routing_edges_to",
    )

    line_type = models.CharField(
        max_length=32,
        choices=LINE_TYPE_CHOICES,
    )

    is_private = models.BooleanField(
        default=False,
        help_text="If true, this edge is only usable in private routes.",
    )

    source_node_id = models.BigIntegerField(
        null=True, blank=True, help_text="pgRouting source node id"
    )
    target_node_id = models.BigIntegerField(
        null=True, blank=True, help_text="pgRouting target node id"
    )

    cost = models.FloatField(default=0.0)
    reverse_cost = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="routing_edges_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="routing_edges_updated",
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "routing_edge"
        indexes = [
            models.Index(fields=["campus", "building", "floor_from", "floor_to"]),
            models.Index(fields=["line_type"]),
            models.Index(fields=["is_private"]),
        ]

    def __str__(self):
        return f"RoutingEdge(id={self.id}, type={self.line_type}, building={self.building_id})"


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


    geom = gis_models.MultiLineStringField(srid=3857, dim=3, spatial_index=True, null=True, blank=True)


    class Meta:
        abstract = True
        ordering = ['network_type']

    def __str__(self):
        return str(self.name) or ''

