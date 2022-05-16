import pytest

from app.functions import check_size_correct, get_status_job


@pytest.mark.parametrize(
    ('size', 'result'),
    [('32', True), ('64', True), ('original', True), ('some string', False)],
)
def test_check_size_correct(size, result):
    assert check_size_correct(size) == result


def test_get_status_job_done(complete_job):
    assert get_status_job(complete_job) == 'DONE'


def test_get_status_job_failed(failed_job):
    assert get_status_job(failed_job) == 'FAILED'


def test_get_status_job_waiting(waiting_job):
    assert get_status_job(waiting_job) == 'WAITING'


def test_get_status_job_in_progress(in_progress_job):
    assert get_status_job(in_progress_job) == 'IN_PROGRESS'
