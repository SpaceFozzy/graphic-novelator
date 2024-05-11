import os
import sys
from generative_models.text_to_text import TextToTextGenerator
from generative_models.text_to_image import TextToImageGenerator
from html_builder.html_builder import generate_chunks_html, generate_index_html

def chunk_text(text, chunk_size=100):
    """
    Yields chunks of text of approximately `chunk_size` words.
    """
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

class GraphicNovel:
    def __init__(self, filename):
        self.filename = filename
        story_directory = os.getenv("STORY_DIR", "./example")
        self.root_directory = f"{story_directory}"
        self.scene_directory = f"{story_directory}/scenes"
        self.pages_directory = f"{story_directory}/pages"
        self.image_directory = f"{story_directory}/images"
        os.makedirs(self.scene_directory, exist_ok=True)
        os.makedirs(self.image_directory, exist_ok=True)

    def read_file(self):
        """
        Reads and returns the content of the file specified by `self.filename`.
        """
        with open(self.filename, "r", encoding="utf-8") as file:
            return file.read()

    def write_scene(self, description, scene_number, overwrite):
        """
        Writes a scene description to a file corresponding to `scene_number`.
        """
        scene_path = os.path.join(self.scene_directory, f"{scene_number}.txt")
        if overwrite or not os.path.exists(scene_path):
            with open(scene_path, "w", encoding="utf-8") as file:
                file.write(description)
            print(f"Scene {scene_number} analysis complete and written to {scene_path}.")

    def generate_image(self, description, scene_number, overwrite):
        """
        Generates an image based on the description, and ensures no overwriting of existing images unless specified.
        """
        image_path = os.path.join(self.image_directory, f"{scene_number}.png")
        if overwrite or not os.path.exists(image_path):
            self.image_generator.generate_image(description, scene_number)
            print(f"Image for scene {scene_number} created at {image_path}.")

    def build(self, specific_chunk=None):
        """
        Builds the graphic novel by generating descriptions and images for each text chunk.
        Skips generation if both scene description and image files exist unless overwriting is specified.
        """
        text = self.read_file()
        generator = TextToTextGenerator()
        # Check if files exist and determine if generation is needed
        descriptions = []
        for i, chunk in enumerate(chunk_text(text)):
            scene_number = i + 1
            scene_path = os.path.join(self.scene_directory, f"{scene_number}.txt")
            image_path = os.path.join(self.image_directory, f"{scene_number}.png")
            overwrite = specific_chunk == scene_number
            if overwrite or not (os.path.exists(scene_path) and os.path.exists(image_path)):
                if os.path.exists(scene_path) and not overwrite:
                    with open(scene_path, "r", encoding="utf-8") as file:
                        description = file.read()
                    descriptions.append((scene_number, description))
                    print(f"Using existing description for scene {scene_number}.")
                else:
                    description = generator.generate(self.create_query_prompt(chunk))
                    descriptions.append((scene_number, description))
                    self.write_scene(description, scene_number, overwrite)
            else:
                print(f"Skipping generation for scene {scene_number}, both files already exist.")

        # Unload the text generator so the image generator can fit on the GPU
        # TODO: Manage the loading/unloading of models more intuitively
        generator.unload()
        self.image_generator = TextToImageGenerator()
        # Process each scene for which description was generated
        for scene_number, description in descriptions:
            overwrite = specific_chunk == scene_number
            self.generate_image(description, scene_number, overwrite)

        os.makedirs(self.pages_directory, exist_ok=True)

        html_pages = generate_chunks_html(list(chunk_text(text)))
        for i, html in enumerate( html_pages ):
            file_path = os.path.join(self.pages_directory, f"{i + 1}.html")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html)
            print(f"HTML for chunk {i + 1} written to {file_path}")

        html = generate_index_html(len(list(chunk_text(text))))
        file_path = os.path.join(self.root_directory, f"index.html")
        with open(file_path, "w", encoding="utf-8") as file:
                file.write(html)
        print(f"HTML index written to {file_path}")

    @staticmethod
    def create_query_prompt(chunk):
        """
        Creates a standardized query prompt from a text chunk for scene description.
        """
        return (
            f"Write a one-sentence description of an interesting visual composition of the passage below. Make the most important subject the first thing you mention. Be concise."
            f"Write only your concise one-sentence description in response:\n\n{chunk}"
        )

if __name__ == "__main__":
    # Determine if a specific scene number has been provided as a command-line argument
    story_directory = os.getenv("STORY_DIR", "./example")
    chunk_number = int(sys.argv[1]) if len(sys.argv) > 1 else None
    novel = GraphicNovel(f"{story_directory}/text.txt")
    novel.build(chunk_number)

