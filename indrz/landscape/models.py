from django.contrib.gis.db import models as gis_models
from django.utils.translation import get_language, ugettext_lazy as _


class BaseLookupDomain(gis_models.Model):
    code = gis_models.CharField(verbose_name=_(u"code value"), max_length=150, null=True, blank=True)
    name = gis_models.CharField(verbose_name=_(u"name descriptive value"), max_length=256, null=True, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.name) or u''

class LtSurfaceType(BaseLookupDomain):
    """
    The type of surface in landscaped or unpaved areas
    """

    # SURFACE_TYPE = (
    #     ('GRASS', _('Grass')),
    #     ('TREES', _('Trees')),
    #     ('MULCH', _('Mulch')),
    #     ('PARKING', _('Parking')),
    #     ('PATH', _('Path')),
    #     ('SIDEWALK', _('Sidewalk')),
    #     ('ROCK', _('Rock')),
    #     ('IVY-GROUNDCOVER', _('Ivy-ground cover')),
    #     ('PLANTER', _('Planter')),
    #     ('OTHER', _('Other')),
    #     ('UNKOWN', _('Unkown')),
    #     ('DIRT', _('Dirt')),
    #     ('SAND', _('Sand')),
    #     ('SPORT_TURF', _('Sport turf')),

    #     )
    #

    pass

class LtMarkingType(BaseLookupDomain):

    # Code	Name
    # Edge line	Edge line
    # Lane line	Lane line
    # Center line	Center line
    # Stop line	Stop line
    # Yield line	Yield line
    # Crosswalk	Crosswalk
    # Arrow	Arrow
    # Word	Word
    # Handicap	Handicap
    # Symbol	Symbol
    # Cross-hatch	Cross-hatch
    # Dotted line	Dotted line
    # Left turn	Left turn
    # Right turn	Right turn
    # U-turn	U-turn
    # Two-way left turn	Two-way left turn
    # Speed hump	Speed hump
    # Parking	Parking
    # Other	Other
    # No Parking	No Parking
    # Limited Parking	Limited Parking
    # Loading/Unloading	Loading/Unloading
    # Lane line double	Lane line double
    # Lane line broken	Lane line broken
    # Lane line dotted	Lane line dotted
    # Center line double	Center line double
    # Center line broken	Center line broken
    # Sports field line	Sports field line
    pass


class LtCondition(BaseLookupDomain):
    #      CONDITION = (
    #     ('EXCELLENT', _('Excellent')),
    #     ('VERY_GOOD', _('Very Good')),
    #     ('FAIR', _('Fair')),
    #     ('POOR', _('Poor')),
    #     ('VERY_POOR', _('Very poor')),
    #     ('UNKNOWN', _('Unknown')),

    #     )
    pass



class LandscapeArea(gis_models.Model):
    """
    The extent of open space (grass, mulch, etc.) and other unpaved areas.
    """

    name = gis_models.CharField(verbose_name=_(u"Name"),
           max_length=256, db_column='name', null=True, blank=True)

    description = gis_models.TextField(verbose_name=_(u"Description"),
        db_column='description', help_text=_(u"Brief description"), null=True, blank=True)
    surface_type = gis_models.CharField(verbose_name=_(u"Surface type"), max_length=256, null=True, blank=True)


    fk_surface_type = gis_models.ForeignKey(LtSurfaceType, null=True, blank=True)
    
    geom_mpoly = gis_models.MultiPolygonField(srid=3857)
    objects = gis_models.GeoManager()


    def __unicode__(self):
        return unicode(self.name) or u''



class PavementMarkLines(gis_models.Model):
    """
    The pavement marking lines delineate vehicular paths of travel along
    the roadway by marking the center of the road, lanes of travel, edges of pavement, etc.
    """

    fk_mark_type = gis_models.ForeignKey(LtMarkingType, null=True, blank=True)
    fk_condition = gis_models.ForeignKey(LtCondition, null=True, blank=True)

    geom_mline = gis_models.MultiLineStringFieldField(srid=3857)
    objects = gis_models.GeoManager()


    def __unicode__(self):
        return unicode(self.fk_mark_type) or u''