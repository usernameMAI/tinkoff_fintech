import pytest
from fakeredis import FakeRedis

fake_redis = FakeRedis()


@pytest.fixture(autouse=True)
def _init_redis():
    yield
    fake_redis.flushdb()
