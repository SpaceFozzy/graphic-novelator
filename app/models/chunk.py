import os
from utils.file import write_file, write_image, read_file, exists

class Chunk:
    def __init__(self, text, number, root_directory):
        self.text = text
        self.number = number
        self.scene_directory = os.path.join(root_directory, "scenes")
        self.images_directory = os.path.join(root_directory, "images")
        self.scene_path = os.path.join(root_directory, f"scenes/{number}.txt")
        self.image_path = os.path.join(root_directory, f"images/{number}.png")
        self.description = None

    def read_description(self):
        if exists(self.scene_path):
            self.description = read_file(self.scene_path)
            return self.description

    def save_description(self, description, overwrite=False):
        os.makedirs(self.scene_directory, exist_ok=True)
        if overwrite or not exists(self.scene_path):
            write_file(self.scene_path, description, overwrite)
            self.description = description
            print(f"Scene {self.number} analysis complete and written to {self.scene_path}")

    def has_description(self):
        description_file_exists = exists(self.scene_path)
        return description_file_exists

    def create_query_prompt(self):
        """
        Creates a standardized query prompt from a text chunk for scene description.
        """
        return (
            f"Write a one-sentence description of an interesting visual composition of the passage below. Make the most important subject the first thing you mention. Be concise."
            f"Write only your concise one-sentence description in response:\n\n{self.text}"
        )

    def ensure_description(self, generator, overwrite=False):
        if not self.has_description() or overwrite:
            query_prompt = self.create_query_prompt()
            self.description = generator.generate(query_prompt)
            self.save_description(self.description, overwrite)
        else:
            self.description = self.read_description()

    def generate_image(self, image_generator, overwrite=False):
        os.makedirs(self.images_directory, exist_ok=True)
        if overwrite or not exists(self.image_path):
            image = image_generator.generate(self.description)
            write_image(self.image_path, image)
            print(f"Image for scene {self.number} created at {self.image_path}")
