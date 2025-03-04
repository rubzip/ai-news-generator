import json

with open("output/news_of_day.json", "r", encoding="utf-8") as file:
    data = json.load(file)

html_content = """<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resumen Diario de Noticias powered with AI</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>\n<body>\n
"""
for i, item in enumerate(data.get("content", [])):
    category, text = item.get("category"), item.get("text")
    
    if i == 0:
        html_content += "<header>\n"
        if category and text:
            html_content += f"<{category}>{text}</{category}>\n"
        if data.get("keywords"):
            keywords = ' '.join(f"<code>{k}</code> " for k in data["keywords"])
            html_content += f'<div style="text-align: center;"><p>{keywords}</p></div>\n'
        html_content += "<header>\n"
    elif category and text:
        html_content += f"<{category}>{text}</{category}>\n"

sources = data.get("sources", [])

if sources:
    html_content += "<h2>Fuentes</h2>\n"
    html_content += "<ul>\n"
    for source, url in sources.items():
        html_content += f'<li><a href="{url}">{source}</a></li>\n'
    html_content += "</ul>\n"
html_content += '</body></html>'


with open("output/news_of_day.html", "w", encoding="utf-8") as file:
    file.write(html_content)