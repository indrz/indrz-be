from django.contrib.gis.db import models as gis_models
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from buildings.models import Building, BuildingFloor


class BookShelf(gis_models.Model):
    """
    The geometry line of a shelfs actual location on floor within a building
    """

    external_id = gis_models.CharField(verbose_name=_('External Shelf ID'), max_length=255)

    geom = gis_models.MultiLineStringField(verbose_name=_("Geometry of shelf"), db_column='geom',
                                           blank=True, null=True, srid=3857, spatial_index=False)

    left_from_label = gis_models.CharField(verbose_name=_("left from label"),
                                      help_text=_("Map left label range shown on the 2d map"), max_length=150,
                                      null=True, blank=True)
    left_to_label = gis_models.CharField(verbose_name=_("left to label"),
                                      help_text=_("Map left label range shown on the 2d map"), max_length=150,
                                      null=True, blank=True)
    right_from_label = gis_models.CharField(verbose_name=_("right from label"),
                                      help_text=_("Map right label range shown on the 2d map"), max_length=150,
                                      null=True, blank=True)
    right_to_label = gis_models.CharField(verbose_name=_("right to label"),
                                      help_text=_("Map right label range shown on the 2d map"), max_length=150,
                                      null=True, blank=True)

    building_floor = gis_models.ForeignKey(BuildingFloor, on_delete=models.CASCADE)
    building = gis_models.ForeignKey(Building, on_delete=models.CASCADE)

    double_sided = gis_models.BooleanField(_("Does the shelf have two sides"), default=True, null=True, blank=True)

    rotation = gis_models.IntegerField(_("Rotation angle of the bookshelf"), null=True, blank=True)
    length = gis_models.DecimalField(verbose_name=_("length in m of bookshelf"), max_digits=10, decimal_places=2,
                                    null=True, blank=True)
    width = gis_models.DecimalField(verbose_name=_("width in m of bookshelf"), max_digits=10, decimal_places=2,
                                    null=True, blank=True)
    depth = gis_models.DecimalField(verbose_name=_("depth in m of bookshelf"), max_digits=10, decimal_places=2,
                                    null=True, blank=True)

    def __str__(self):
        return self.external_id or ''


class ShelfData(models.Model):
    """
    Shelf Data represents the table of data collected by the library.

    This contains the ranges of each shelf and the measures to
    locate a single book with in a section on a shelf.

    Note NO geometry is stored in this table.
    """
    SHELF_SIDE = (
        (_('L'), _('Left')),
        (_('R'), _('Right')),
    )
    external_id = models.CharField(verbose_name=_('External Shelf ID'), max_length=150)
    floor = models.IntegerField(verbose_name=_('Floor Number'), null=True)

    section_main = models.CharField(verbose_name=_('Main Section'), max_length=150, blank=True, null=True,
                                    help_text=_('Library Code for a section with multiple shelves'))
    section_child = models.CharField(verbose_name=_('Sub Section'), max_length=150, blank=True, null=True,
                                     help_text=_('Library Code for a sub- section'))

    section = models.CharField(verbose_name=_('External Shelf Section'), max_length=150,
                               help_text=_('A section located within a single shelf'), null=True, blank=True)

    system_from = models.CharField(verbose_name=_('Shelving System Start Value'), max_length=150)
    system_to = models.CharField(verbose_name=_('Shelving System End Value'), max_length=150)

    sys_from_array = ArrayField(
        ArrayField(
            models.CharField(max_length=150, null=True, blank=True)
        ), null=True
    )
    sys_to_array = ArrayField(
        ArrayField(
            models.CharField(max_length=150, null=True, blank=True)
        ), null=True
    )

    side = models.CharField(verbose_name=_('Left or Right side'), max_length=10, choices=SHELF_SIDE, null=True)
    measure_from = models.DecimalField(verbose_name=_('Distance from measure'), decimal_places=2, max_digits=5, null=True, blank=True)
    measure_to = models.DecimalField(verbose_name=_('Distance end measure'), decimal_places=2, max_digits=5, null=True, blank=True)

    bookshelf = models.ForeignKey(BookShelf, on_delete=models.CASCADE, null=True, blank=True)
    building_floor = gis_models.ForeignKey(BuildingFloor, on_delete=models.CASCADE, null=True, blank=True)
    building = gis_models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)

    system_from_jsonb= JSONField(null=True, blank=True)
    system_to_jsonb= JSONField(null=True, blank=True)

    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def section_length(self):
        if self.measure_to and self.measure_from:
            return self.measure_to - self.measure_from
        else:
            return ''

    @property
    def combined_id(self):
        if self.external_id and self.floor and self.section:
            return self.external_id + str(self.floor) + self.section + self.pk + self.section
        else:
            return ''

    def __str__(self):
        return self.combined_id or ''


# class BookShelf(gis_models.Model):
#     """
#     A bookshelf located on the floor within a building
#     """
#     name = gis_models.CharField(verbose_name=_("Name"), max_length=150, null=True, blank=True)
#     external_id = gis_models.CharField(verbose_name=_("external_id"),
#                                        help_text=_("External ID used by the library to uniquely identify a shelf"),
#                                        max_length=150, null=True, blank=True)
#     id_letter = gis_models.CharField(verbose_name=_("id shelf letter label"), max_length=150, null=True, blank=True)
#
#     section_id = gis_models.CharField(verbose_name=_("Section id"), help_text=_("A section is a small area on a shelf"),
#                                       max_length=150, null=True, blank=True)
#     section_from = gis_models.DecimalField(_("Section start meter value"), decimal_places=2)
#     section_to = gis_models.DecimalField(_("Section start meter value"), decimal_places=2)
#
#     system_from = gis_models.CharField(verbose_name=_("Classification system start range value"), max_length=150,
#                                        null=True, blank=True)
#     system_to = gis_models.CharField(verbose_name=_("Classification system end range value"), max_length=150, null=True,
#                                      blank=True)
#
#     sign_display_from = gis_models.CharField(verbose_name=_("Classification system start range value"), max_length=150,
#                                              null=True, blank=True)
#     sign_disply_to = gis_models.CharField(verbose_name=_("Classification system end range value"), max_length=150,
#                                           null=True, blank=True)
#
#     double_faced = gis_models.BooleanField(_("Does the shelf have two sides"), default=True)
#     vertical_position = gis_models.IntegerField(_("The row position"),
#                                                 help_text=_("The shelf vertical order from bottom 0  to top N"))
#
#     collection = gis_models.CharField(verbose_name=_("Name of collection the shelf belongs to"), null=True, blank=True)
#
#     left_label = gis_models.CharField(verbose_name=_("left label"),
#                                       help_text=_("Map left label range shown on the 2d map"), max_length=150,
#                                       null=True, blank=True)
#     right_label = gis_models.CharField(verbose_name=_("right label"),
#                                       help_text=_("Map right label range shown on the 2d map"), max_length=150,
#                                       null=True, blank=True)
#
#     length = gis_models.DecimalField(verbose_name=_("length in m"), max_digits=10, decimal_places=2, null=True,
#                                      blank=True)
#     length_section = gis_models.DecimalField(verbose_name=_("section lenght in cm"), max_digits=10, decimal_places=2,
#                                              null=True, blank=True)
#
#     width = gis_models.DecimalField(verbose_name=_("width in cm of shelf"), max_digits=10, decimal_places=2, null=True,
#                                     blank=True)
#     depth = gis_models.DecimalField(verbose_name=_("depth in cm of shelf"), max_digits=10, decimal_places=2, null=True,
#                                     blank=True)
#
#     fk_building_floor = gis_models.ForeignKey(BuildingFloor)
#     fk_building = gis_models.ForeignKey(Building)
#
#     def start_label(self):
#         """
#         Assumes the user would be looking down the shelf
#         geometry from Linestring StartPoint to EndPoint
#
#         Generates the label for the start side of the shelf
#         including the classification system from  and to value
#
#         Return the START From-To label from the right side and
#         Return the START From-To label from the left side
#         :return:
#         """
#         pass
#
#     def end_label(self):
#         """
#         Assumes the user would be looking down the shelf
#         geometry from Linestring EndPoint to StartPoint
#
#         Generates the label for the end side of the shelf
#         including the classification system from  and to value
#
#         Return the END From-To label from the right side and
#         Return the END From-To label from the left side
#         :return:
#         """
#         #
#
#         pass
#
#     def __str__(self):
#         return self.name or ''

