import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_api_docs(logged_in):
    response = logged_in.client.get(reverse('docs'))

    assert response.status_code == 200
