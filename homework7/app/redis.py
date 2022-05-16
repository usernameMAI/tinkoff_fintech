import redis  # type: ignore

HISTORY_SIZE = 49
CLIENT_ID_SIZE = 13

r = redis.Redis(host='redis', port=6379, decode_responses=False)


def add_message_to_redis(client_id: int, data: str) -> None:
    r.lpush('messages', f'{client_id}: {data}')
    r.ltrim('messages', 0, HISTORY_SIZE)


def get_last_messages() -> str:
    messages = r.lrange('messages', 0, HISTORY_SIZE)
    data = ''
    for message in messages:
        message_str = message.decode()
        data += (
            "'Client #"
            + message_str[0:CLIENT_ID_SIZE]
            + ' says'
            + message_str[CLIENT_ID_SIZE:]
            + "'"
        )
    return data
