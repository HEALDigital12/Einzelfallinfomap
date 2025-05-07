import React, { useEffect, useState } from 'react';
import L from 'leaflet';

function CrimeMap({ selectedTypes, selectedYear }) {
  const [map, setMap] = useState(null);
  const [data, setData] = useState({ faelle: [] });

  useEffect(() => {
    const newMap = L.map('map').setView([51.1657, 10.4515], 6);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap-Mitwirkende & CartoDB',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(newMap);

    setMap(newMap);

    // Funktion zum Abrufen und Anzeigen der Daten
    const fetchDataAndRender = () => {
      fetch('/data/faelle_2025.json')
        .then(res => res.json())
        .then(newData => {
          setData(newData);
          newMap.eachLayer(layer => {
            if (layer instanceof L.CircleMarker && layer !== tileLayer) {
              newMap.removeLayer(layer);
            }
          });
          newData.faelle.forEach(fall => {
            const jahr = new Date(fall.datum).getFullYear();
            if (jahr === selectedYear && selectedTypes.includes(fall.delikt)) {
              const marker = L.circleMarker(fall.koordinaten, {
                radius: 8,
                color: fall.farbe,
                fillColor: fall.farbe,
                fillOpacity: 0.9
              }).addTo(newMap);
              marker.bindPopup(
                `<strong>${fall.delikt}</strong><br>${fall.ort}<br>${fall.datum}<br><a href="${fall.quelle}" target="_blank">Zur Quelle</a>`
              );
            }
          });
        });
    };

    // Rufe die Daten beim ersten Laden ab
    fetchDataAndRender();

    // Richte ein Intervall ein, um die Daten alle X Minuten neu abzurufen (z.B. alle 5 Minuten)
    const intervalId = setInterval(fetchDataAndRender, 5 * 60 * 1000); // 5 Minuten

    // Gib eine Bereinigungsfunktion zurück, um das Intervall zu stoppen, wenn die Komponente unmounted wird
    return () => {
      if (map) {
        map.remove();
      }
      clearInterval(intervalId);
    };
  }, [selectedTypes, selectedYear]); // Abhängigkeiten bleiben gleich, da wir periodisch neu laden

  return (
    <div id="map" style={{ height: '100vh', width: '100%' }}></div>
  );
}

export default CrimeMap;
