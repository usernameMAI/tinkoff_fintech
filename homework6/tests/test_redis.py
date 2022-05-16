from mock import patch

from app.convert import convert_bytes_to_image, decode_bytes_base64
from app.redis import compress_images


def test_compress_images(tinkoff_image):
    with patch('PIL.Image.open') as mock:
        mock.return_value = tinkoff_image
        images = compress_images(tinkoff_image)
    image = convert_bytes_to_image(decode_bytes_base64(images['imageoriginal']))
    image32 = convert_bytes_to_image(decode_bytes_base64(images['image32']))
    image64 = convert_bytes_to_image(decode_bytes_base64(images['image64']))
    assert image.size == (800, 800)
    assert image32.size == (32, 32)
    assert image64.size == (64, 64)
