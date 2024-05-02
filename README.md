# Graphic Novelator

This project takes the text of a story and tries to use generative AI to build a graphic novel
experience of it.

Right now the plan is to:
1. ✅Chunk the text
2. ✅Iterate through the text and build a scene list with details
3. ✅Generate images for those scenes
4. Serve the data and images as static assets from a web page

# Getting Started

1. `pip install langchain langchain-openai diffusers transformers`
2. Add your story as text.txt
3. `python3 start.py` will start generating scene descriptions and images for the whole story, with one image per 500 word chunk of text
4. `python3 start.py 17` will regenerate the scene description and image for the 17th chunk
