import logging
from typing import Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from app.connection import ConnectionManager
from app.html import html
from app.redis import add_message_to_redis, get_last_messages

FILE_LOGS_NAME = 'logs.log'

router = APIRouter()
manager = ConnectionManager()
logging.basicConfig(level=logging.DEBUG, filename=FILE_LOGS_NAME, filemode='w')
my_logger = logging.getLogger(__name__)


@router.get('/')
async def get() -> HTMLResponse:
    return HTMLResponse(html)


@router.websocket('/ws/{client_id}')  # pragma: no cover
async def websocket_endpoint(websocket: WebSocket, client_id: int) -> None:
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            add_message_to_redis(client_id, data)
            my_logger.debug('Client #%d says: %s.', client_id, data)

            await manager.send_personal_message(f'You wrote: {data}', websocket)
            await manager.broadcast(f'Client #{client_id} says: {data}')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f'Client #{client_id} left the chat')


@router.get('/last_messages')
async def last_messages() -> Dict[str, str]:
    return {'messages': get_last_messages()}
