## Graphic Novelator

This project takes the text of a story and tries to use generative AI to build a graphic novel
experience of it.

## Creating Your Own Story
Before you begin, make a new empty directory somewhere for your project. Place the raw text of story in your project folder as `text.txt`

1. In the graphic-novelator directory, start a virtual environment: `python3 -m venv .env`
2. Activate your virtual environment: `source .env/bin/activate` (`deactivate` to deactivate it)
3. Install the dependencies: `pip install -r requirements.txt`
4. `TITLE="Your Title" AUTHOR="Author" STORY_DIR="../my-story" python3 app/start.py` will start generating scene descriptions, images, and html pages for the whole story, with one image per 100 word chunk of text
5. `TITLE="Your Title" AUTHOR="Author" STORY_DIR="../my-story" python3 app/start.py 17` will regenerate the scene description and image for the 17th chunk

## Requirements
1. Python
2. A CUDA-enabled GPU (or a lot of patience)
3. Access to the [Llama 3 8b Instruct model via HuggingFace](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) (it's a "gated model" so you must request access) or the willingness to switch the text-to-text model.
4. A text file of your story (if you want to generate a new one)

## Examples

### Full Stories
* [H.P. Lovecraft's "The Colour Out of Space"](https://spacefozzy.github.io/graphic-novelator/example/pages/1.html)
* [H.P. Lovecraft's "The Festival"](https://spacefozzy.github.io/the-festival-illustrated/pages/1.html)

### Single Scene (Mary Shelley's Frankenstein)

#### Scene Description
`A lone explorer stands at the edge of a frozen lake, the aurora borealis dancing across the dark sky behind him, as the icy landscape stretches out to the horizon, with the faint outline of a ship in the distance.`

#### Image
Not sure why he's drifting on an iceberg but its a start 😛
![1](https://github.com/SpaceFozzy/graphic-novelator/assets/10606414/44b10ee9-2382-4188-8897-572d27547d9f)
