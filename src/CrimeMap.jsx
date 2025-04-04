
import React, { useEffect } from 'react';
import L from 'leaflet';

function CrimeMap({ selectedTypes, selectedYear }) {
  useEffect(() => {
    const map = L.map('map').setView([51.1657, 10.4515], 6);

    const tileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap-Mitwirkende & CartoDB',
      subdomains: 'abcd',
      maxZoom: 19
    });
    tileLayer.addTo(map);

    fetch('/data/faelle_2025.json')
      .then(res => res.json())
      .then(data => {
        data.faelle.forEach(fall => {
          const jahr = new Date(fall.datum).getFullYear();
          if (jahr === selectedYear && selectedTypes.includes(fall.delikt)) {
            const marker = L.circleMarker(fall.koordinaten, {
              radius: 8,
              color: fall.farbe,
              fillColor: fall.farbe,
              fillOpacity: 0.9
            }).addTo(map);
            marker.bindPopup(
              `<strong>${fall.delikt}</strong><br>${fall.ort}<br>${fall.datum}<br><a href="${fall.quelle}" target="_blank">Zur Quelle</a>`
            );
          }
        });
      });

    return () => {
      map.remove();
    };
  }, [selectedTypes, selectedYear]);

  return (
    <div id="map" style={{ height: '100vh', width: '100%' }}></div>
  );
}

export default CrimeMap;
