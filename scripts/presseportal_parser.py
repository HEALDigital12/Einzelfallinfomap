from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://www.presseportal.de"


def extract_article_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/blaulicht/pm/" in href:
            links.append(urljoin(BASE_URL, href))
    return sorted(set(links))
