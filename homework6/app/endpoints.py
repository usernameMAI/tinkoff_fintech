from http import HTTPStatus
from io import BytesIO
from typing import Dict, Union

from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.convert import convert_bytes_to_image, decode_bytes_base64
from app.functions import check_size_correct, get_status_job
from app.redis import compress_images, queue

router = APIRouter()


@router.post('/tasks', status_code=HTTPStatus.CREATED)
def add_task(file: UploadFile) -> Dict[str, int]:
    task = queue.enqueue(compress_images, file.file, result_ttl=60 * 60)
    return {'task-id': task.id}


@router.get('/tasks/{task_id}', status_code=HTTPStatus.OK)
def get_task_status(task_id: str) -> Union[Dict[str, Union[str, int]], HTTPException]:
    task = queue.fetch_job(task_id)
    if not task:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not exists')
    return {'task-id': task.id, 'status': get_status_job(task)}


@router.get('/tasks/{task_id}/image', status_code=HTTPStatus.OK)
def get_task(task_id: str, size: str) -> Union[StreamingResponse, HTTPException]:
    task = queue.fetch_job(task_id)
    if not task:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not exists')
    if not check_size_correct(size):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Not correct size'
        )
    decode_image_in_bytes = decode_bytes_base64(task.result[f'image{size}'])
    image = convert_bytes_to_image(decode_image_in_bytes)
    image_byte_arr = BytesIO()
    image.save(image_byte_arr, 'png')
    image_byte_arr.seek(0)
    return StreamingResponse(image_byte_arr, media_type='image/png')
