import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL de Xataka Ciberseguridad
URL = "https://www.clubolimpia.com.py/noticias"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

items = []

# Buscar titulares reales: enlaces dentro de h2
links = soup.select("h2 a")

for link in links[:10]:
    title = link.get_text(strip=True)
    href = link.get("href")
    if title and href:
        items.append(f"""
        <item>
            <title>{title}</title>
            <link>{href}</link>
            <pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
            <guid>{href}</guid>
        </item>
        """)

# Guardar RSS en la raíz del repositorio
with open("rss.xml", "w", encoding="utf-8") as f:
    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Mi RSS automático</title>
    <link>{URL}</link>
    <description>Titulares automáticos</description>
    {''.join(items)}
</channel>
</rss>
"""
    f.write(rss_content)
