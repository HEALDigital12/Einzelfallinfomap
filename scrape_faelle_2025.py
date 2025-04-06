#!/usr/bin/env python3

import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time

# Konfiguration
SUCHBEGRIFFE = ["Messer", "Raub", "Tötung", "Körperverletzung", "Überfall", "Gewalt"]
MAX_FAELLE = 50
HEUTE = datetime.now().strftime("%d.%m.%Y")
ERGEBNIS_DATEI = "public/data/faelle_2025.json"

# Geokodierung per OpenStreetMap
def geokodiere(ort):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={ort}, Deutschland"
    try:
        response = requests.get(url, headers={"User-Agent": "HEALDIGITAL-Scraper"})
        daten = response.json()
        if daten:
            return [float(daten[0]["lat"]), float(daten[0]["lon"])]
    except:
        pass
    return [0.0, 0.0]

# Presseportal-Scraping
def finde_faelle():
    ergebnisse = []
    seite = 1

    while len(ergebnisse) < MAX_FAELLE:
        url = f"https://www.presseportal.de/blaulicht/stichwort/kriminalitaet?pagenr={seite}"
        response = requests.get(url, headers={"User-Agent": "HEALDIGITAL-Scraper"})
        soup = BeautifulSoup(response.text, "html.parser")
        beitraege = soup.select(".news")

        if not beitraege:
            break

        for eintrag in beitraege:
            datum_raw = eintrag.select_one(".news-date") 
            titel_raw = eintrag.select_one(".news-title")
            link_raw = eintrag.select_one("a")

            if not (datum_raw and titel_raw and link_raw):
                continue

            datum = datum_raw.text.strip()
            titel = titel_raw.text.strip()
            link = "https://www.presseportal.de" + link_raw["href"]

            if datum != HEUTE:
                continue

            if not any(wort.lower() in titel.lower() for wort in SUCHBEGRIFFE):
                continue

            ort = titel.split(":")[0].strip()
            koords = geokodiere(ort)
            farbe = "red"

            ergebnisse.append({
                "delikt": titel,
                "ort": ort,
                "datum": datetime.now().strftime("%Y-%m-%d"),
                "quelle": link,
                "koordinaten": koords,
                "farbe": farbe
            })

            if len(ergebnisse) >= MAX_FAELLE:
                break

            time.sleep(1)  # höfliche Pause für Nominatim

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
