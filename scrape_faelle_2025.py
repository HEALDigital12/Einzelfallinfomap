#!/usr/bin/env python3

import os
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
    "Gewalt": ["gewalt"],
    "Verkehrsunfall": ["unfall", "zusammenstoß", "verletzte"],
    "Einbruch": ["einbruch", "eingebrochen"]
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
                    "Gewalt": "blue",
                    "Verkehrsunfall": "lightblue",
                    "Einbruch": "brown"
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
    return None # Gebe None zurück, wenn die Geokodierung fehlschlägt

def scrape_rss_feeds(rss_urls):
    ergebnisse = []
    logging.info("+++ RSS-Feed-Scraping gestartet +++")
    for url in rss_urls:
        logging.info(f"Verarbeite RSS-Feed: {url}")
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                titel = entry.title
                logging.info(f"  Titel des Eintrags: {titel}")
                delikt, farbe = get_delikt_und_farbe(titel)
                logging.info(f"  Erkanntes Delikt: {delikt}")
                if delikt != "Sonstiges":
                    orte_titel = finde_orte_nlp(titel)
                    orte_beschreibung = finde_orte_nlp(getattr(entry, 'description', ''))
                    orte = list(set(orte_titel + orte_beschreibung))
                    logging.info(f"  Gefundene Orte (Titel): {orte_titel}")
                    logging.info(f"  Gefundene Orte (Beschreibung): {orte_beschreibung}")

                    datum_obj = getattr(entry, 'published_parsed', getattr(entry, 'updated_parsed', None))
                    link = entry.link

                    if datum_obj:
                        beitrags_datum = datetime(*datum_obj[:3]).date()
                        # Überdenke die Datumsfilterung - jetzt etwas großzügiger
                        if beitrags_datum < HEUTE - timedelta(days=3) or beitrags_datum > HEUTE + timedelta(days=1):
                            continue

                        # Versuche, den ersten gefundenen Ort zu geokodieren
                        koords = None
                        if orte:
                            for ort in orte:
                                koords = geokodiere(ort)
                                if koords:
                                    break # Nimm den ersten erfolgreich geokodierten Ort

                        if koords:
                            ergebnisse.append({
                                "delikt": delikt,
                                "ort": orte[0] if orte else None, # Speichere den ersten gefundenen Ort
                                "datum": beitrags_datum.strftime("%Y-%m-%d"),
                                "quelle": link,
                                "koordinaten": koords,
                                "farbe": farbe
                            })
                        else:
                            logging.warning(f"Konnte keinen Ort für Eintrag '{titel}' geokodieren.")
                    else:
                        logging.warning(f"Konnte Datum für Eintrag '{titel}' nicht parsen.")

        except Exception as e:
            logging.error(f"Fehler beim RSS-Feed '{url}': {e}")
        time.sleep(1)
    return ergebnisse

def main():
    logging.info("+++ main() gestartet +++")
    rss_feed_faelle = scrape_rss_feeds(RSS_FEED_URLS)
    logging.info(f"Anzahl der extrahierten Fälle: {len(rss_feed_faelle)}")
    alle_faelle = rss_feed_faelle

    daten = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "faelle": alle_faelle
    }

    logging.info(f"Daten zum Schreiben: {daten}")

    os.makedirs(os.path.dirname(ERGEBNIS_DATEI), exist_ok=True)

    with open(ERGEBNIS_DATEI, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)

    logging.info(f"Daten erfolgreich geschrieben nach: {ERGEBNIS_DATEI}")

if __name__ == "__main__":
    main()
