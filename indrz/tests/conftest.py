import shutil
import types
from io import BytesIO

import pytest
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from users.factories import UserFactory


def create_image(size: tuple = (100, 100), image_mode: str = 'RGB', image_format: str = 'JPEG'):
    """
    Generate a test image
    """
    data = BytesIO(b'test')
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    return data


def _logged_in(client, monkeypatch) -> types.SimpleNamespace:
    """
    Client with already logged in user to make authenticated requests.
    :param client:
    :param monkeypatch:
    :return: types.SimpleNamespace
    """
    monkeypatch.setattr('indrz.users.ModelPermissions.has_permission', lambda *args, **kwargs: True)

    user = UserFactory.create()
    client.login(username=user.username, password=user.username)

    result = types.SimpleNamespace()
    result.client = client
    result.user = user

    return result


logged_in = pytest.fixture(_logged_in)


@pytest.fixture
def logged_in_superuser(client, monkeypatch):
    """
    Client with already logged in superuser to make authenticated requests.
    :param client:
    :param monkeypatch:
    :return: types.SimpleNamespace
    """
    result = _logged_in(client, monkeypatch)
    result.user.is_superuser = True
    result.user.save()

    return result


@pytest.fixture
def image_file() -> callable:
    def create_image_file(filename='image.jpeg'):
        image = create_image()
        return SimpleUploadedFile(filename, image.getvalue(), content_type='image/jpeg')

    return create_image_file


def pytest_sessionfinish(session, exitstatus):
    shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
