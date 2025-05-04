#!/usr/bin/env python3

import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time
import logging
from geopy.geocoders import Nominatim

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
MAX_FAELLE = 20  # Erhöhe die Anzahl, um mehr potenzielle Fälle zu finden
HEUTE = datetime.now().date()
ERGEBNIS_DATEI = "public/data/faelle_2025.json"
USER_AGENT = "HEALDIGITAL-Scraper"
NOMINATIM_DELAY = 1  # Sekunde Pause zwischen Geocoding-Anfragen
GEOLOCATOR = Nominatim(user_agent=USER_AGENT, timeout=5)

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

# Geokodierung per OpenStreetMap mit Fehlerbehandlung
def geokodiere(ort):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={ort}, Deutschland"
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
        response.raise_for_status()  # Wirft eine Exception für HTTP-Fehler
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

# Presseportal-Scraping
def finde_faelle():
    ergebnisse = []
    seite = 1

    while len(ergebnisse) < MAX_FAELLE:
        # Spezifischere Suche nach Blaulicht-Meldungen
        url = f"https://www.presseportal.de/blaulicht/nr/alle/seite/{seite}"
        try:
            response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            beitraege = soup.select(".news")

            if not beitraege:
                logging.info(f"Keine weiteren Beiträge auf Seite {seite} gefunden.")
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
                    # Datum des Beitrags parsen (Format kann variieren)
                    beitrags_datum = datetime.strptime(datum_str, '%d.%m.%Y').date()
                    # Nur heutige oder gestrige Meldungen berücksichtigen (um keine alten Fälle zu ziehen)
                    if beitrags_datum < HEUTE - timedelta(days=1) or beitrags_datum > HEUTE:
                        continue
                except ValueError:
                    logging.warning(f"Konnte Datum '{datum_str}' nicht parsen.")
                    continue

                delikt, farbe = get_delikt_und_farbe(titel)
                if delikt != "Sonstiges":
                    # Versuche, den Ort aus dem Titel zu extrahieren (verbesserte Logik)
                    ort_teile = titel.split(" - ")[0].split(": ")[-1].split(",")[0].strip()
                    koords = geokodiere(ort_teile)

                    ergebnisse.append({
                        "delikt": delikt,
                        "ort": ort_teile,
                        "datum": beitrags_datum.strftime("%Y-%m-%d"),
                        "quelle": link,
                        "koordinaten": koords,
                        "farbe": farbe
                    })

                    if len(ergebnisse) >= MAX_FAELLE:
                        break

            time.sleep(1)  # Höfliche Pause

        except requests.exceptions.RequestException as e:
            logging.error(f"Fehler beim Abrufen von '{url}': {e}")
            break
        except Exception as e:
            logging.error(f"Unerwarteter Fehler beim Scrapen von '{url}': {e}")
            break

        seite += 1

    return ergebnisse

# Hauptfunktion
def main():
    faelle = finde_faelle()

    daten = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "faelle": faelle
    }

    with open(ERGEBNIS_DATEI, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
