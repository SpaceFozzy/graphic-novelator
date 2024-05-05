import os


def generate_index_html(total_chunks):
    title = os.getenv("TITLE", "Unknown Story")
    author = os.getenv("AUTHOR", "Unknown Author")

    html = "<html>"
    html += f"<head><title>{title}</title></head>"
    html += "<body>"
    html += f"<h1>{title}</h1>"
    html += f"<p>By {author}</p>"
    html += f"<p>Built with <a href='https://github.com/SpaceFozzy/graphic-novelator'>graphic-novelator<a></p>"
    html += "<ul>"
    for i in range(1, total_chunks + 1):
        html += f"<li><a href='pages/{i}.html'>Scene {i}</a></li>"
    html += "</ul>"
    html += "</body>"
    html += "</html>"
    return html

def generate_chunks_html(chunks):
    total_chunks = len(chunks)
    html_pages = []

    for i in range(total_chunks):
        html = """
<html>
<head>
    <style>
        body {
            background-color: black;
            color: white;
            font-size: 48px; /* Increased text size for better readability */
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
        }
        img {
            display: block;
            max-width: 100%;
            margin: 0 auto;
        }
        .content-container {
            max-width: 800px; /* Typical blog width */
            margin: 0 auto;
            padding: 20px;
        }
        .navigation {
            font-family: 'Bangers', sans-serif;
            text-decoration: none;
            color: white;
            font-size: 72px; /* Larger font size for mobile touch */
            padding: 10px; /* Added padding for easier touch */
            display: block;
            margin: 20px auto; /* Centered horizontally */
            text-align: center;
        }
        .back {
            text-align: left;
        }
        .next {
            text-align: right;
        }

        /* Media Query for Desktop Screens */
        @media (min-width: 1024px) {
            body {
                font-size: 24px; /* Half size on desktop */
            }
            .navigation {
                font-size: 36px; /* Half size on desktop */
            }
        }
    </style>
    <link href="https://fonts.googleapis.com/css?family=Bangers&display=swap" rel="stylesheet">
</head>
<body>
        """

        chunks_per_page = 5
        limit = min(i + chunks_per_page, total_chunks)  # Ensuring we do not go out of bounds

        # Back navigation button
        if i > 0:
            prev_page = max(i - chunks_per_page, 0)
            html += f"<div class='content-container'><a href='{prev_page}.html' class='navigation back'>Back</a></div>"

        for j in range(i, limit):
            html += f"<img src='../images/{j + 1}.png'>"
            html += f"<div class='content-container'><p>{chunks[j]}</p></div>"

        # Next navigation button
        if i < total_chunks - chunks_per_page:
            next_page = i + chunks_per_page
            html += f"<div class='content-container'><a href='{next_page}.html' class='navigation next'>Next</a></div>"

        html += "</body></html>"
        html_pages.append(html)

    return html_pages

