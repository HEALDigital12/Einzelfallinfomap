import React, { useEffect, useState, useRef } from 'react';
import L from 'leaflet';

function CrimeMap({ selectedTypes, selectedYear }) {
  const mapRef = useRef(null);
  const markerLayerRef = useRef(null);
  const [data, setData] = useState({ faelle: [] });

  // Initialisiere Karte nur einmal
  useEffect(() => {
    const map = L.map('map').setView([51.1657, 10.4515], 6);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap-Mitwirkende & CartoDB',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(map);

    mapRef.current = map;
    markerLayerRef.current = L.layerGroup().addTo(map);

    return () => {
      map.remove();
    };
  }, []);

  // Daten laden und Marker aktualisieren (Filterung deaktiviert)
  useEffect(() => {
    if (!mapRef.current) return;

    const fetchDataAndRender = () => {
      fetch('/data/faelle_2025.json')
        .then(res => res.json())
        .then(newData => {
          setData(newData);

          // Bestehende Marker entfernen
          markerLayerRef.current.clearLayers();

          // Alle neuen Marker hinzufügen (Filterung ignoriert)
          newData.faelle.forEach(fall => {
            const marker = L.circleMarker(fall.koordinaten, {
              radius: 8,
              color: fall.farbe,
              fillColor: fall.farbe,
              fillOpacity: 0.9
            }).bindPopup(
              `<strong>${fall.delikt}</strong><br>${fall.ort}<br>${fall.datum}<br><a href="${fall.quelle}" target="_blank">Zur Quelle</a>`
            );
            markerLayerRef.current.addLayer(marker);
          });
        })
        .catch(err => console.error('Fehler beim Laden der Daten:', err));
    };

    fetchDataAndRender();
    const intervalId = setInterval(fetchDataAndRender, 5 * 60 * 1000); // 5 Minuten

    return () => clearInterval(intervalId);
  }, []); // Abhängigkeitsarray ist jetzt leer

  return <div id="map" style={{ height: '100vh', width: '100%' }}></div>;
}

export default CrimeMap;
