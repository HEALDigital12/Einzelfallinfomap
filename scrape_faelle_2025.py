#!/usr/bin/env python3

import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time
import logging
from geopy.geocoders import Nominatim
import feedparser
from google.cloud import language_v1
from google.cloud.language_v1.types import Document, Entity

# Logging einrichten
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Konfiguration
SUCHBEGRIFFE_DELIKT = {
    "Tötung": ["tötung", "mord", "totschlag"],
    "Körperverletzung": ["körperverletzung", "schlag", "tritt", "attacke"],
    "Sexualdelikt": ["vergewaltigung", "sexueller übergriff", "belästigung"],
    "Messerstecherei": ["messerstecherei", "messerangriff"],
    "Raub": ["raub", "überfall"],
    "Gewalt": ["gewalt"]
}

MAX_FAELLE = 100
HEUTE = datetime.now().date()
ERGEBNIS_DATEI = "public/data/faelle_2025.json"
USER_AGENT = "HEALDIGITAL-Scraper"
NOMINATIM_DELAY = 1
GEOLOCATOR = Nominatim(user_agent=USER_AGENT, timeout=5)
RSS_FEED_URLS = [
    "https://www.presseportal.de/rss/polizei.rss2"
]

def finde_orte_nlp(text):
    client = language_v1.LanguageServiceClient()
    document = Document(content=text, type=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(request={"document": document})
    orte = [entity.name for entity in response.entities if entity.type == Entity.Type.LOCATION]
    return orte

def get_delikt_und_farbe(titel):
    for delikt, keywords in SUCHBEGRIFFE_DELIKT.items():
        for keyword in keywords:
            if keyword in titel.lower():
                farbzuordnung = {
                    "Tötung": "red",
                    "Körperverletzung": "orange",
                    "Sexualdelikt": "violet",
                    "Messerstecherei": "darkred",
                    "Raub": "yellow",
                    "Gewalt": "blue"
                }
                return delikt, farbzuordnung.get(delikt, "gray")
    return "Sonstiges", "gray"

def geokodiere(ort):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={ort}, Deutschland"
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
        response.raise_for_status()
        daten = response.json()
        if daten and len(daten) > 0:
            return [float(daten[0]["lat"]), float(daten[0]["lon"])]
    except requests.exceptions.RequestException as e:
        logging.error(f"Fehler beim Geokodieren von '{ort}': {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Fehler beim Decodieren der Geokodierungsantwort für '{ort}': {e}")
    except Exception as e:
        logging.error(f"Unerwarteter Fehler beim Geokodieren von '{ort}': {e}")
    return [0.0, 0.0]

def scrape_presseportal():
    ergebnisse = []
    seite = 1

    while len(ergebnisse) < MAX_FAELLE:
        url = f"https://www.presseportal.de/blaulicht/nr/alle/seite/{seite}"
        try:
            response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            beitraege = soup.select(".news")

            if not beitraege:
                logging.info(f"Keine weiteren Beiträge auf Seite {seite}.")
                break

            for eintrag in beitraege:
                datum_raw = eintrag.select_one(".news-date")
                titel_raw = eintrag.select_one(".news-title")
                link_raw = eintrag.select_one("a")

                if not (datum_raw and titel_raw and link_raw):
                    continue

                datum_str = datum_raw.text.strip()
                titel = titel_raw.text.strip()
                link = "https://www.presseportal.de" + link_raw["href"]

                try:
                    beitrags_datum = datetime.strptime(datum_str, '%d.%m.%Y').date()
                    if beitrags_datum < HEUTE - timedelta(days=1) or beitrags_datum > HEUTE:
                        continue
                except ValueError:
                    logging.warning(f"Konnte Datum '{datum_str}' nicht parsen.")
                    continue

                delikt, farbe = get_delikt_und_farbe(titel)
                if delikt != "Sonstiges":
                    orte = finde_orte_nlp(titel)
                    ort = orte[0] if orte else None

                    if ort:
                        koords = geokodiere(ort)
                        ergebnisse.append({
                            "delikt": delikt,
                            "ort": ort,
                            "datum": beitrags_datum.strftime("%Y-%m-%d"),
                            "quelle": link,
                            "koordinaten": koords,
                            "farbe": farbe
                        })

                if len(ergebnisse) >= MAX_FAELLE:
                    break

                time.sleep(1)

        except requests.exceptions.RequestException as e:
            logging.error(f"Fehler beim Abrufen von Seite {seite}: {e}")
            break
        except Exception as e:
            logging.error(f"Unerwarteter Fehler auf Seite {seite}: {e}")
            break

        seite += 1

    return ergebnisse

def scrape_rss_feeds(rss_urls):
    ergebnisse = []
    logging.info("+++ RSS-Feed-Scraping gestartet +++")
    for url in rss_urls:
        logging.info(f"Verarbeite RSS-Feed: {url}")
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                titel = entry.title
                logging.info(f"  Titel des Eintrags: {titel}")  # Zeige den Titel
                delikt, farbe = get_delikt_und_farbe(titel)
                logging.info(f"  Erkanntes Delikt: {delikt}")  # Zeige das erkannte Delikt
                if delikt != "Sonstiges":
                    orte = finde_orte_nlp(titel)
                    logging.info(f"  Gefundene Orte: {orte}")  # Zeige die gefundenen Orte
                    ort = orte[0] if orte else None

                    if ort:
                        koords = geokodiere(ort)
                        ergebnisse.append({
                            "delikt": delikt,
                            "ort": ort,
                            "datum": beitrags_datum.strftime("%Y-%m-%d"),
                            "quelle": link,
                            "koordinaten": koords,
                            "farbe": farbe
                        })

        except Exception as e:
            logging.error(f"Fehler beim RSS-Feed '{url}': {e}")
        time.sleep(1)
    return ergebnisse

def main():
    presseportal_faelle = scrape_presseportal()
    rss_feed_faelle = scrape_rss_feeds(RSS_FEED_URLS)
    alle_faelle = presseportal_faelle + rss_feed_faelle

    daten = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "faelle": alle_faelle
    }

    with open(ERGEBNIS_DATEI, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
