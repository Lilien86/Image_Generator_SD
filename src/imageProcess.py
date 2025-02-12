from PIL import Image
import torch
import io
import requests
import PIL
import requests
from io import BytesIO

def resize_image(image, max_width=1024, max_height=1024):
    width, height = image.size

    aspect_ratio = width / height

    if width > height:
        new_width = min(width, max_width)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = min(height, max_height)
        new_width = int(new_height * aspect_ratio)

    resized_img = image.resize((new_width, new_height), Image.LANCZOS)

    print(f"\n\nwidth: {new_width}, and height: {new_height}\n\n")
    return resized_img

def convert_to_png(image):
    buffer = io.BytesIO()
    buffer.seek(0)
    return buffer

def download_image(url):
        response = requests.get(url)
        return PIL.Image.open(BytesIO(response.content)).convert("RGB")