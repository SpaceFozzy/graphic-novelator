## Graphic Novelator

This project takes the text of a story and tries to use generative AI to build a graphic novel
experience of it.

Next steps:
1. ✅ Add some styling to the pages
2. Allow generating a story in another location
3. ✅ Get dependencies under control (use a virtual environment)
4. Clean up the code

## Creating Your Own Story

1. Start a virtual environment: `python -m venv .env`
2. Activate your virtual environment: `source .env/bin/activate` (`deactivate` to deactivate it)
3. Install the dependencies: `pip install -r requirements.txt`
4. Delete everything in `./example` and add your story as `example/text.txt`
5. `TITLE="Your Title" AUTHOR="Author" python3 start.py` will start generating scene descriptions, images, and html pages for the whole story, with one image per 100 word chunk of text
6. `TITLE="Your Title" AUTHOR="Author" python3 start.py 17` will regenerate the scene description and image for the 17th chunk

## Examples

### Full Stories
[H.P. Lovecraft's The Colour Out of Space](https://spacefozzy.github.io/graphic-novelator/example/pages/1.html)

### Single Scene (Mary Shelley's Frankenstein)

#### Scene Description
`A lone explorer stands at the edge of a frozen lake, the aurora borealis dancing across the dark sky behind him, as the icy landscape stretches out to the horizon, with the faint outline of a ship in the distance.`

#### Image
Not sure why he's drifting on an iceberg but its a start 😛
![1](https://github.com/SpaceFozzy/graphic-novelator/assets/10606414/44b10ee9-2382-4188-8897-572d27547d9f)
