
import React from 'react';

function Filter({ selectedTypes, onChange }) {
  const types = [
    { value: 'Tötungsdelikt', label: 'Tötungsdelikt' },
    { value: 'Messerstecherei', label: 'Messerstecherei / Körperverletzung' },
    { value: 'Raubüberfall', label: 'Raub' },
    { value: 'Vergewaltigung', label: 'Sexualdelikt' }
  ];

  const handleCheckboxChange = (value) => {
    if (selectedTypes.includes(value)) {
      onChange(selectedTypes.filter(type => type !== value));
    } else {
      onChange([...selectedTypes, value]);
    }
  };

  return (
    <div style={{
      position: 'absolute',
      top: '20px',
      left: '20px',
      backgroundColor: '#222',
      color: 'white',
      padding: '10px',
      borderRadius: '8px',
      fontSize: '14px',
      zIndex: 1000
    }}>
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
