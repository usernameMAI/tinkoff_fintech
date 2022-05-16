from typing import Dict, TextIO

from PIL import Image
from redis import Redis
from rq import Queue

from app.convert import encode_image_base64

redis_conn = Redis()
queue = Queue(connection=redis_conn)


def compress_images(image: TextIO) -> Dict[str, bytes]:
    open_image = Image.open(image)
    image_in_bytes = encode_image_base64(open_image)
    image_in_bytes_32 = encode_image_base64(open_image.resize((32, 32)))
    image_in_bytes_64 = encode_image_base64(open_image.resize((64, 64)))
    images_item = {
        'imageoriginal': image_in_bytes,
        'image32': image_in_bytes_32,
        'image64': image_in_bytes_64,
    }
    return images_item
