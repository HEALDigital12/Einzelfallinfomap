import React from 'react';

function Legend() {
  const legendItems = [
    { color: 'red', label: 'Tötungsdelikt' },
    { color: 'darkred', label: 'Messerstecherei' },
    { color: 'yellow', label: 'Raub' },
    { color: 'violet', label: 'Sexualdelikt' }
    // Füge hier weitere schwere Straftaten und ihre Farben hinzu
  ];

  return (
    <div style={{
      position: 'absolute',
      bottom: '20px',
      right: '20px',
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
