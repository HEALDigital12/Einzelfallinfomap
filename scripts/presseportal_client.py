import requests

BASE_URL = "https://www.presseportal.de"
HEADERS = {"User-Agent": "HEALDIGITAL-EinzelfallInfoMap/1.0"}


def build_search_url(query, page=1):
    return f"{BASE_URL}/suche/{query}/blaulicht/{page}"


def fetch_html(url):
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.text
