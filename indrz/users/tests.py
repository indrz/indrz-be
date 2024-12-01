from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Songs
from .serializers import UserSerializer
from .models import User

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_user(username="", email="", password=""):
        if username != "" and email != "" and password != "":
            User.objects.create(username=username, email=email, password=password)

    def setUp(self):
        # add test data
        self.create_user("spiderman", "spin@gmail.com", "airborne")


class GetAllUsersTest(BaseViewTest):

    def test_get_all_users(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("users-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = User.objects.all()
        serialized = UserSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)