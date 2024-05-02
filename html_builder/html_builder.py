import os

def generate_index_html(total_chunks):
    title = os.getenv('TITLE', 'Unknown Story')
    author = os.getenv('AUTHOR', 'Unknown Author')

    html = "<html>"
    html += f"<head><title>{title}</title></head>"
    html += "<body>"
    html += f"<h1>{title}</h1>"
    html += f"<p>By {author}</p>"
    html += f"<p>Built with <a href='https://github.com/SpaceFozzy/graphic-novelator'>graphic-novelator<a></p>"
    html += "<ul>"
    for i in range(1, total_chunks + 1):
        html += f"<li><a href='{i}.html'>Scene {i}</a></li>"
    html += "</ul>"
    html += "</body>"
    html += "</html>"
    return html

def generate_chunk_html(chunk, scene_number, total_chunks):
    html = "<html>"
    html += f"<img src='../images/{scene_number}.png'>"
    if scene_number != 1:
        html += f"<a href='{scene_number - 1}.html'>Previous</a>"
    if scene_number != total_chunks:
        html += f"<a href='{scene_number + 1}.html'>Next</a>"
    html += f"<div><h1>Scene {scene_number}</h1><p>{chunk}</p></div>"
    html += "</html>"
    return html

