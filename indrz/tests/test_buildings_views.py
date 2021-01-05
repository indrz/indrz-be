from rest_framework import status

from ..buildings.models import Organization
from ..buildings.serializers import OrganizationSerializer


class GetSingleOrganizationTest(TestCase):
    """ Test module for GET single puppy API """

    def setUp(self):
        self.casper = Organization.objects.create(
            name='Casper', age=3, breed='Bull Dog', color='Black')

    def test_get_valid_single_puppy(self):
        response = client.get(
            reverse('get_delete_update_puppy', kwargs={'pk': self.rambo.pk}))
        organization = Organization.objects.get(pk=self.rambo.pk)
        serializer = OrganizationSerializer(puppy)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
