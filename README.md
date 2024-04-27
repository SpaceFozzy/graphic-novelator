# Graphic Novelator

This project takes the text of a story and tries to use generative AI to build a graphic novel
experience of it.

Right now the plan is to:
1. Chunk the text (done)
2. Iterate through the text and build a scene list with details (done)
3. Generate images for those scenes
4. Serve the data and images as static assets from a web page

# Getting Started

1. `pip install langchain langchain-openai`
2. Add your story as text.txt
3. `python3 start.py`
