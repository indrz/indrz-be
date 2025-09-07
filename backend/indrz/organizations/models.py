from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class BaseName(models.Model):
    """
    physical base address information of a building
    """
    name = models.CharField(verbose_name=_("Name"), max_length=256, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name) or ''


class AddressBase(models.Model):
    """
    physical base address information of a building
    """
    street = models.CharField(verbose_name=_("Street"), max_length=256,
                              blank=True, null=True)
    house_number = models.CharField(verbose_name=_("Building or house number"), max_length=10,
                                    blank=True, null=True)
    postal_code = models.CharField(verbose_name=_("Postal code"), max_length=8,
                                   blank=True, null=True)
    municipality = models.CharField(verbose_name=_("Municipality"),
                                    blank=True, null=True,
                                    max_length=256)
    city = models.CharField(verbose_name=_("City"),
                            blank=True, null=True,
                            max_length=256)

    country = models.CharField(verbose_name=_("Country"),
                               blank=True, null=True,
                               max_length=256)

    class Meta:
        abstract = True
        ordering = ['city']

    def __str__(self):
        return str(self.city) or ''


class InfoBase(BaseName, AddressBase):
    description = models.TextField(verbose_name=_("Description"),
                                   help_text=_("Brief description"), null=True, blank=True)
    phone = models.CharField(verbose_name=_("Phone"), max_length=32,
                             blank=True, null=True)
    email = models.EmailField(verbose_name=_("Email"), max_length=256,
                              blank=True, null=True)
    website = models.URLField(verbose_name=_("Website"), max_length=256, blank=True, null=True)
    geom = models.PointField(verbose_name=_("Building centroid for small scale maps"),
                             blank=True, null=True, srid=3857, spatial_index=False)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return str(self.name) or ''


class Organization(InfoBase):
    """
    Represents a customer or Uni that has one or more building locations

    """
    owner = models.CharField(verbose_name=_("Owner name"), max_length=128, null=True, blank=True)
    legal_form = models.CharField(verbose_name=_("Legal entity form"), max_length=128, null=True, blank=True)


# ---------------------------------------------------------------------
# Department model referencing geodata.tu_user_departments
# ---------------------------------------------------------------------
class Department(InfoBase, models.Model):

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name_en = models.TextField(null=True, blank=True)
    name_de = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=10, null=True, blank=True)
    color = models.CharField(max_length=10, null=True, blank=True)

    ext_dept_id = models.IntegerField(null=True, blank=True)
    ext_dept_code = models.CharField(max_length=50, null=True, blank=True)
    ext_parent_dept_code = models.CharField(max_length=50, null=True, blank=True)
    ext_parent_dept_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name or ''