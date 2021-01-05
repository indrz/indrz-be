from django.test import TestCase
from buildings.models import Organization


class OrganizationTest(TestCase):
    """ Test module for Organization model """

    def setUp(self):
        Organization.objects.create(
            name='RedCompany', description="somefoo")
        Organization.objects.create(
            name='BlueCompany', description="morefoo")

    def test_new_company(self):
        blue_company = Organization.objects.get(name='RedCompany')
        self.assertEqual(
            blue_company.name, "BlueCompany")
