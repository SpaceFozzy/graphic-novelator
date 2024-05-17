import os
from PIL import Image

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def write_file(path, content, overwrite=True):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        create_directory(directory)
    if overwrite or not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

def write_image(path, image):
    image.save(path)

def exists(*paths):
    return all(os.path.exists(path) for path in paths)
