import React from 'react';

function Legend() {
  const legendItems = [
    { color: 'lightblue', label: 'Verkehrsunfall' },
    { color: 'brown', label: 'Einbruch' },
    // Füge hier weitere Legenden-Einträge hinzu
  ];

  return (
    <div style={{
      position: 'absolute',
      bottom: '20px', // Passe diese Werte nach Bedarf an
      right: '20px',  // Passe diese Werte nach Bedarf an
      backgroundColor: '#222',
      color: 'white',
      padding: '10px',
      borderRadius: '8px',
      fontSize: '14px',
      zIndex: 1000
    }}>
      <strong>Legende</strong>
      <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
        {legendItems.map((item, idx) => (
          <li key={idx} style={{ marginTop: '4px' }}>
            <span style={{
              display: 'inline-block',
              width: '12px',
              height: '12px',
              backgroundColor: item.color,
              marginRight: '8px',
              verticalAlign: 'middle'
            }}></span>
            {item.label}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Legend;
