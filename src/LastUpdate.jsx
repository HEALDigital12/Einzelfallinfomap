
import React, { useEffect, useState } from 'react';

function LastUpdate() {
  const [lastUpdate, setLastUpdate] = useState(null);

  useEffect(() => {
    fetch('/data/faelle_2025.json')
      .then(res => res.json())
      .then(data => {
        const date = new Date(data.last_updated);
        setLastUpdate(date.toLocaleString('de-DE', {
          day: '2-digit',
          month: 'long',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }));
      });
  }, []);

  return (
    <div style={{
      position: 'absolute',
      bottom: '20px',
      left: '20px',
      backgroundColor: '#222',
      color: 'white',
      padding: '8px',
      borderRadius: '6px',
      fontSize: '13px',
      zIndex: 1000
    }}>
      {lastUpdate ? `Letztes Update: ${lastUpdate}` : 'Lade Aktualisierungsdatum...'}
    </div>
  );
}

export default LastUpdate;
