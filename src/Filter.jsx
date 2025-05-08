import React from 'react';

function Filter({ selectedTypes, onChange }) {
  const types = [
    { value: 'Verkehrsunfall', label: 'Verkehrsunfall' },
    { value: 'Einbruch', label: 'Einbruch' },
    // Füge hier weitere Filter-Optionen hinzu, entsprechend den Delikttypen in deiner JSON-Datei.
    // Stelle sicher, dass 'value' exakt mit dem Wert in 'fall.delikt' übereinstimmt.
  ];

  const handleCheckboxChange = (value) => {
    if (selectedTypes.includes(value)) {
      onChange(selectedTypes.filter(type => type !== value));
    } else {
      onChange([...selectedTypes, value]);
    }
  };

  return (
    <div style={{ /* ... (deine Styles) ... */ }}>
      <strong>Filter</strong>
      {types.map((type, idx) => (
        <div key={idx}>
          <label>
            <input
              type="checkbox"
              checked={selectedTypes.includes(type.value)}
              onChange={() => handleCheckboxChange(type.value)}
              style={{ marginRight: '6px' }}
            />
            {type.label}
          </label>
        </div>
      ))}
    </div>
  );
}

export default Filter;
