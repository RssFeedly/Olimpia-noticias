import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.clubolimpia.com.py/news"
BASE_URL = "https://www.clubolimpia.com.py"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

try:
    response = requests.get(URL, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    items = []

    # 🔥 Selector principal más robusto (Elementor + WordPress común)
    articles = soup.select("a[href*='/news/']")

    # 🔄 Fallback si no encuentra nada
    if not articles:
        articles = soup.find_all("a", href=True)
        articles = [
            a for a in articles
            if "/news/" in a["href"] and len(a.get_text(strip=True)) > 10
        ]

    print(f"ARTÍCULOS ENCONTRADOS: {len(articles)}")

    for link_tag in articles[:10]:
        title = link_tag.get_text(strip=True)
        href = link_tag.get("href")

        if not title or not href:
            continue

        # 🔗 URL absoluta segura
        full_link = href if href.startswith("http") else f"{BASE_URL}{href}"

        # 🔒 Filtro final correcto
        if "/news/" not in full_link:
            continue

        items.append(f"""
        <item>
            <title><![CDATA[{title}]]></title>
            <link>{full_link}</link>
            <pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
            <guid isPermaLink="true">{full_link}</guid>
            <description>Noticia oficial del Club Olimpia</description>
        </item>
        """)

    if not items:
        print("DEBUG: No se encontraron noticias. Posible cambio en estructura HTML.")

    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Club Olimpia - Noticias</title>
    <link>{URL}</link>
    <description>Actualidad del Decano</description>
    <language>es-py</language>
    <lastBuildDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>
    {''.join(items)}
</channel>
</rss>
"""

    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(rss_content)

    print(f"Éxito: {len(items)} noticias procesadas.")

except Exception as e:
    print(f"Error crítico: {e}")
