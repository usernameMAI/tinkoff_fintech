import pytest
from fakeredis import FakeStrictRedis
from mock import MagicMock, patch
from PIL import Image
from rq import Queue

from app.redis import compress_images

queue = Queue(is_async=False, connection=FakeStrictRedis())


@pytest.fixture
def complete_job():
    mock = MagicMock()
    mock.get_status.return_value = 'finished'
    return mock


@pytest.fixture
def failed_job():
    mock = MagicMock()
    mock.get_status.return_value = 'failed'
    return mock


@pytest.fixture
def in_progress_job():
    mock = MagicMock()
    mock.get_status.return_value = 'started'
    return mock


@pytest.fixture
def waiting_job():
    mock = MagicMock()
    mock.get_status.return_value = 'queued'
    return mock


@pytest.fixture
def tinkoff_image():
    image = Image.open('tests/images/tinkoff.png')
    return image


@pytest.fixture
def file_image():
    with open('tests/images/tinkoff.png', 'rb') as file:
        yield file


@pytest.fixture(scope='session')
def job():
    image = Image.open('tests/images/tinkoff.png')
    with patch('PIL.Image.open') as mock:
        mock.return_value = image
        return queue.enqueue(compress_images, image)
