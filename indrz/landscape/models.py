from django.contrib.gis.db import models as gis_models
from django.utils.translation import ugettext_lazy as _
from buildings.models import Campus, LtAccessType


class BaseLookupDomain(gis_models.Model):
    code = gis_models.CharField(verbose_name=_("code value"), max_length=150, null=True, blank=True)
    name = gis_models.CharField(verbose_name=_("name value"), max_length=256, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['code',]

    def __str__(self):
        return str(self.name) or ''

        
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

class LtPavementMarkingType(BaseLookupDomain):
    """"
    The type of pavement marking along the roadway or within paved areas
    """

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

class LtPavementSurfaceType(BaseLookupDomain):
    """
    The type of pavement surface
    """
    # PAVEMENT_SURFACE_TYPE = (
    #     ('Concrete', _('Concrete')),
    #     ('Asphalt', _(' Asphalt')),
    #     ('Chip and Seal', _('Chip and Seal')),
    #     ('Gravel' , _('Gravel')),
    #     ('Brickpaver' , _('Brickpaver')),
    #     ('Cobblestone' , _('Cobblestone')),
    #     ('Other' , _('Other')),
    #     ('Unknown' , _('Unknown')),
    #     ('Athletic Track' , _('Athletic Track')),
    #     ('Hardcourt' , _('Hardcourt'))
    #     )
    pass

        
class LtPavementSurfaceUse(BaseLookupDomain):
    """
    The primary use of the paved surface
    """
    # Street Street 
    # Walking Path Walking Path 
    # Sidewalk Sidewalk 
    # Bike Path Bike Path 
    # Parking Lot Parking Lot 
    # Curb / Gutter Curb / Gutter 
    # Unknown Unknown 
    # Other Other 
    # Curb Curb 
    # Gutter Gutter 
    # Athletic Track Athletic Track 
    pass
    
    
class LtAmenityType(BaseLookupDomain):
    pass
    # AMENITY_TYPE = (
    #     ('VEGETATION', _('Vegetation')),
    #     ('BENCH', _('Bench')),
    #     ('BIKE PARKING', _('Bike Parking')),
    #     ('GATE' , _('Gate')),
    #     ('FENCE' , _('Fence')),
    #     ('WALL' , _('Wall')),
    #     ('Other' , _('Other')),
    #     ('Unknown' , _('Unknown'))
    #     )
    # Tree
    # Bench
    # Bike Parking
    # Aluminum Perimeter Fence Aluminum Perimeter Fence 
    # Automatic Gate Automatic Gate 
    # Chain Link Fence Chain Link Fence 
    # Decorative Wall Decorative Wall 
    # Gate Gate 
    # Retaining Wall Retaining Wall 
    # Security Chain Link Fence Security Chain Link Fence 
    # Wooden Picket Fence Wooden Picket Fence 
    # Wooden Post and Rail Fence Wooden Post and Rail Fence 
    # Wooden Privacy Fence Wooden Privacy Fence 
    # Wooden Split Rail Fence Wooden Split Rail Fence 
    # Wrought Iron Fence Wrought Iron Fence 
    # Other Other 
    # Unknown Unknown 

class LandscapeArea(gis_models.Model):
    """
    The extent of open space (grass, mulch, etc.) and other unpaved areas.
    """

    name = gis_models.CharField(verbose_name=_("Name"),
           max_length=256, db_column='name', null=True, blank=True)

    description = gis_models.TextField(verbose_name=_("Description"),
        db_column='description', help_text=_("Brief description"), null=True, blank=True)

    fk_surface_type = gis_models.ForeignKey(LtSurfaceType , on_delete=gis_models.CASCADE, null=True, blank=True)
    fk_campus = gis_models.ForeignKey(Campus, on_delete=gis_models.CASCADE)

    geom_mpoly = gis_models.MultiPolygonField(verbose_name=_("Geometry multi-polygon outside facility areas"), db_column='geom',
                             blank=True, null=True, srid=3857, spatial_index=True)


    def __str__(self):
        return str(self.name) or ''


class LandscapeAmenityLine(gis_models.Model):
    """
    The collective set of landscape and other amenities installed
    on a site for various purposes, including fences, gates,
    retaining walls, and decorative walls.s.
    """

    name = gis_models.CharField(verbose_name=_("Name"),
           max_length=256, db_column='name', null=True, blank=True)

    description = gis_models.TextField(verbose_name=_("Description"),
        db_column='description', help_text=_(u"Brief description"), null=True, blank=True)


    fk_amenity_type = gis_models.ForeignKey(LtAmenityType, on_delete=gis_models.CASCADE, null=True, blank=True)
    fk_campus = gis_models.ForeignKey(Campus, on_delete=gis_models.CASCADE)

    geom_mline = gis_models.MultiLineStringField(verbose_name=_("Geometry multi-linestrings outside area lines"),
                                                 db_column='geom', blank=True, null=True, srid=3857, spatial_index=True)


    def __str__(self):
        return str(self.name) or ''


class PavementMarkLines(gis_models.Model):
    """
    The pavement marking lines delineate vehicular paths of travel along
    the roadway by marking the center of the road, lanes of travel, edges of pavement, etc.
    """

    fk_mark_type = gis_models.ForeignKey(LtPavementMarkingType, on_delete=gis_models.CASCADE, null=True, blank=True)
    fk_condition = gis_models.ForeignKey(LtCondition, on_delete=gis_models.CASCADE, null=True, blank=True)

    geom_mline = gis_models.MultiLineStringField(verbose_name=_("Geometry multi-linestrings pavement lines"),
                                                 db_column='geom', blank=True, null=True, srid=3857, spatial_index=True)

    def __str__(self):
        return str(self.fk_mark_type) or ''