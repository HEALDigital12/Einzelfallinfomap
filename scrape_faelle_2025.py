#!/usr/bin/env python3
# scrape_faelle_2025.py
import json
from datetime import datetime

data = {
    "last_updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "faelle": [
        {
            "delikt": "Tötungsdelikt",
            "ort": "Berlin Neukölln",
            "datum": "2025-04-01",
            "quelle": "https://presseportal.de/beispiel",
            "koordinaten": [52.4795, 13.4386],
            "farbe": "red"
        }
    ]
}

with open("public/data/faelle_2025.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
