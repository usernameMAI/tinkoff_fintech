from mock import patch

from app.redis import add_message_to_redis, get_last_messages
from tests.conftest import fake_redis


@patch('app.redis.r', fake_redis)
def test_add_message_to_redis():
    add_message_to_redis(12345, 'test')
    assert fake_redis.lrange('messages', 0, 1)[0].decode() == '12345: test'


@patch('app.redis.r', fake_redis)
def test_get_last_messages_with_empty_redis():
    message = get_last_messages()
    assert message == ''


@patch('app.redis.r', fake_redis)
def test_get_last_messages():
    id_client = 1234512345123
    data = 'test'
    add_message_to_redis(id_client, data)
    message = get_last_messages()
    assert message == f"'Client #{id_client} says: {data}'"
