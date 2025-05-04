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
        # Karte ohne Marker erstellen, zentriert auf Deutschland
        karte = folium.Map(location=[51.5, 10.4], zoom_start=6)
    else:
        # Durchschnittliche Koordinaten für den Kartenmittelpunkt berechnen
        latitudes = [fall['koordinaten'][0] for fall in faelle if fall.get('koordinaten')]
        longitudes = [fall['koordinaten'][1] for fall in faelle if fall.get('koordinaten')]

        if latitudes and longitudes:
            mittelpunkt_lat = sum(latitudes) / len(latitudes)
            mittelpunkt_lon = sum(longitudes) / len(longitudes)
            karte = folium.Map(location=[mittelpunkt_lat, mittelpunkt_lon], zoom_start=7)
        else:
            # Fallback, falls keine gültigen Koordinaten vorhanden sind
            karte = folium.Map(location=[51.5, 10.4], zoom_start=6)

        for fall in faelle:
            koords = fall.get('koordinaten')
            if koords and koords != [0.0, 0.0]:
                delikt = fall.get('delikt', 'Unbekannt')
                ort = fall.get('ort', 'Unbekannt')
                datum_str = fall.get('datum', 'Unbekannt')
                quelle = fall.get('quelle', '#')
                farbe = fall.get('farbe', 'gray')

                popup_text = f"<b>{delikt}</b><br>Ort: {ort}<br>Datum: {datum_str}<br><a href='{quelle}' target='_blank'>Quelle</a>"
                folium.CircleMarker(
                    location=koords,
                    radius=8,
                    color=farbe,
                    fill=True,
                    fill_color=farbe,
                    fill_opacity=0.7,
                    popup=popup_text
                ).add_to(karte)

    # Mapbox Tiles hinzufügen (ersetze YOUR_MAPBOX_ACCESS_TOKEN)
    folium.TileLayer(
        tiles='https://api.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}',
        attr='Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id='mapbox.streets',  # oder eine andere Mapbox Style-ID wie 'mapbox.dark' oder 'mapbox.outdoors'
        accessToken='YOUR_MAPBOX_ACCESS_TOKEN',
        zoom_offset=0,
        opacity=0.7,
        detectRetina=True
    ).add_to(karte)

    karte.save(karte_pfad)
    print(f"Karte erfolgreich erstellt und gespeichert in '{karte_pfad}'.")

if __name__ == '__main__':
    karte_erstellen()
