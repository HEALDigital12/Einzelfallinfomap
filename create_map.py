import json
import folium
from datetime import datetime

# Pfad zur JSON-Datei mit den Fällen
daten_pfad = 'public/data/faelle_2025.json'
# Pfad zur HTML-Datei der Karte
karte_pfad = 'public/index.html'

def karte_erstellen():
    try:
        with open(daten_pfad, 'r', encoding='utf-8') as f:
            daten = json.load(f)
    except FileNotFoundError:
        print(f"Fehler: Datei '{daten_pfad}' nicht gefunden.")
        return
    except json.JSONDecodeError:
        print(f"Fehler: Ungültiges JSON-Format in '{daten_pfad}'.")
        return

    faelle = daten.get('faelle', [])

    if not faelle:
        print("Keine Fälle zum Anzeigen auf der Karte gefunden.")
        karte = folium.Map(location=[51.5, 10.4], zoom_start=6, tiles="CartoDB dark_matter")
    else:
        # Mittelpunkt berechnen
        latitudes = [fall['koordinaten'][0] for fall in faelle if fall.get('koordinaten') and fall['koordinaten'] != [0.0, 0.0]]
        longitudes = [fall['koordinaten'][1] for fall in faelle if fall.get('koordinaten') and fall['koordinaten'] != [0.0, 0.0]]

        if latitudes and longitudes:
            mittel_lat = sum(latitudes) / len(latitudes)
            mittel_lon = sum(longitudes) / len(longitudes)
            karte = folium.Map(location=[mittel_lat, mittel_lon], zoom_start=6, tiles="CartoDB dark_matter")
        else:
            karte = folium.Map(location=[51.5, 10.4], zoom_start=6, tiles="CartoDB dark_matter")

        for fall in faelle:
            koords = fall.get('koordinaten')
            if koords and koords != [0.0, 0.0]:
                delikt = fall.get('delikt', 'Unbekannt')
                ort = fall.get('ort', 'Unbekannt')
                datum = fall.get('datum', 'Unbekannt')
                quelle = fall.get('quelle', '#')
                farbe = fall.get('farbe', 'gray')

                popup = f"<b>{delikt}</b><br>Ort: {ort}<br>Datum: {datum}<br><a href='{quelle}' target='_blank'>Quelle</a>"

                folium.CircleMarker(
                    location=koords,
                    radius=7,
                    color=farbe,
                    fill=True,
                    fill_color=farbe,
                    fill_opacity=0.8,
                    popup=popup
                ).add_to(karte)

    # Karte speichern
    karte.save(karte_pfad)
    print(f"✔️ Karte erfolgreich erstellt: {karte_pfad}")

if __name__ == '__main__':
    karte_erstellen()
