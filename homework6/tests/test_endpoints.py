from http import HTTPStatus

from fastapi.testclient import TestClient
from mock import MagicMock, patch

from app.app import app
from tests.conftest import queue

client = TestClient(app)


def test_add_task(file_image):
    with patch('app.endpoints.queue.enqueue') as mock:
        enqueue_return_mock = MagicMock()
        enqueue_return_mock.id = 'some kind of id'
        mock.return_value = enqueue_return_mock
        response = client.post('/tasks', files={'file': file_image})
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {'task-id': 'some kind of id'}


def test_get_task_status(job):
    with patch('app.endpoints.queue.fetch_job') as mock:
        mock.return_value = queue.fetch_job(job.id)
        response = client.get('/tasks/{job.id}')
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'status': 'DONE', 'task-id': job.id}
        mock.return_value = None
        response = client.get('/tasks/123')
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'Task not exists'}


def test_get_task(job):
    with patch('app.endpoints.queue.fetch_job') as mock:
        mock.return_value = queue.fetch_job(job.id)
        response = client.get('/tasks/{job.id}/image', params={'size': 32})
        assert response.status_code == HTTPStatus.OK
        response = client.get('/tasks/{job.id}/image', params={'size': 322})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        mock.return_value = queue.fetch_job(job.id + 'not_found')
        response = client.get('/tasks/{job.id}/image', params={'size': 32})
        assert response.status_code == HTTPStatus.NOT_FOUND
