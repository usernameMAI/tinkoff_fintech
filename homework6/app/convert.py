import base64
from io import BytesIO

from PIL import Image


def convert_image_to_bytes(image: Image) -> bytes:
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()


def convert_bytes_to_image(image: bytes) -> Image:
    img_byte_arr = BytesIO(image)
    return Image.open(img_byte_arr)


def encode_image_base64(image: Image) -> bytes:
    image_in_bytes = convert_image_to_bytes(image)
    encoded_image = base64.b64encode(image_in_bytes)
    return encoded_image


def decode_bytes_base64(task: bytes) -> bytes:
    decode_image = base64.b64decode(task)
    return decode_image
