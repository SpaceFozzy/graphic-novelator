import os
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

def chunk_text(text, chunk_size=500):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i: i + chunk_size])

class GraphicNovel:
    def __init__(self):
        self.validate_env_vars()

    @staticmethod
    def validate_env_vars():
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

    def read_file(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    def write_scene(self, output_stream, scene_number):
        scene_directory = "./scenes"
        os.makedirs(scene_directory, exist_ok=True)  # Ensure the directory exists
        filename = f"{scene_directory}/{scene_number}.txt"
        with open(filename, "w") as file:
            for output in output_stream:
                file.write(output)
        print(f"Chunk {scene_number} scene analysis complete.")

    def build(self):
        text = self.read_file("text.txt")
        for i, chunk in enumerate(chunk_text(text)):
            scene_query_prompt = ChatPromptTemplate.from_template(
                """
                Identify and describe the details of the setting in the following passage:

                {chunk}
                """
            )
            scene_query_chain = (
                scene_query_prompt
                | ChatOpenAI(model_name="gpt-3.5-turbo")
                | StrOutputParser()
            )
            output_stream = scene_query_chain.stream({"chunk": chunk})
            self.write_scene(output_stream, i+1)

if __name__ == "__main__":
    graphic_novelator = GraphicNovel()
    graphic_novelator.build()

