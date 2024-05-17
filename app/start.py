import os
import sys
from generative_models.text_to_text import TextToTextGenerator
from generative_models.text_to_image import TextToImageGenerator
from models.chunk import Chunk
from models.html_builder import HtmlBuilder


def chunk_text(text, chunk_size=100):
    """
    Yields chunks of text of approximately `chunk_size` words.
    """
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i : i + chunk_size])


class GraphicNovel:
    def __init__(self, source_text_file):
        story_directory = os.getenv("STORY_DIR", "./example")
        self.root_directory = f"{story_directory}"
        self.source_text_file = source_text_file

    def read_source_text_file(self):
        """
        Reads and returns the content of the file specified by `self.source_text_file`.
        """
        with open(self.source_text_file, "r", encoding="utf-8") as file:
            return file.read()

    def build(self, specific_chunk=None):
        """
        Builds the graphic novel by generating descriptions and images for each text chunk.
        Skips generation if both scene description and image files exist unless overwriting is specified.
        """
        # Instantiating the text-to-text model will load it to the GPU
        text = self.read_source_text_file()
        text_to_text_generator = TextToTextGenerator()

        # Prepare the story chunk classes
        chunks = [
            Chunk(text, index + 1, self.root_directory)
            for index, text in enumerate(chunk_text(text))
        ]

        # Extract scene descriptions for chunks where needed and save to disk
        for chunk in chunks:
            force_regenerate = specific_chunk == chunk.number
            chunk.ensure_description(
                text_to_text_generator,
                force_regenerate,
            )

        # Unload the text to text model so the GPU has room to fit the text to image model
        text_to_text_generator.unload()
        # Instantiating the text-to-image model will load it to the GPU
        text_to_image_generator = TextToImageGenerator()

        # Generate images for descriptions where needed and save to disk
        for chunk in chunks:
            force_regenerate = specific_chunk == chunk.number
            chunk.generate_image(text_to_image_generator, force_regenerate)

        html_builder = HtmlBuilder(self.root_directory)
        html_builder.generate_html_pages(chunks)
        html_builder.generate_index_html(chunks)

if __name__ == "__main__":
    # Determine if a specific scene number has been provided as a command-line argument
    story_directory = os.getenv("STORY_DIR", "./example")
    chunk_number = int(sys.argv[1]) if len(sys.argv) > 1 else None
    novel = GraphicNovel(f"{story_directory}/text.txt")
    novel.build(chunk_number)
