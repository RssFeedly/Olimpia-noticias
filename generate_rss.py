import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL de noticias del Olimpia
URL = "https://www.clubolimpia.com.py/noticias"
BASE_URL = "https://www.clubolimpia.com.py"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    # El Olimpia suele usar artículos con una clase específica o estructuras dentro de 'post'
    # Ajustamos el selector para ser más precisos con su estructura actual
    articles = soup.find_all('div', class_='post-item') or soup.select("h2 a")

    for article in articles[:10]:
        # Si 'article' es el tag 'a', lo usamos directo. Si es el 'div', buscamos el 'a'.
        link_tag = article if article.name == 'a' else article.find('a')
        
        if link_tag:
            title = link_tag.get_text(strip=True)
            href = link_tag.get("href")
            
            # Validar y completar URL si es relativa
            full_link = href if href.startswith("http") else f"{BASE_URL}{href}"
            
            if title and href:
                items.append(f"""
        <item>
            <title><![CDATA[{title}]]></title>
            <link>{full_link}</link>
            <pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
            <guid isPermaLink="true">{full_link}</guid>
            <description>Noticia de Club Olimpia: {title}</description>
        </item>""")

    # Generar el archivo final
    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>Club Olimpia - Noticias</title>
    <link>{URL}</link>
    <description>Últimas noticias oficiales del Club Olimpia</description>
    <language>es-py</language>
    {''.join(items)}
</channel>
</rss>"""

    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(rss_content)
    print(f"RSS generado con {len(items)} noticias.")

except Exception as e:
    print(f"Error al generar el RSS: {e}")
