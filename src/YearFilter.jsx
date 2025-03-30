
import React from 'react';

function YearFilter({ selectedYear, onChange }) {
  const years = [2025, 2024, 2023, 2022, 2021, 2020];

  return (
    <div style={{
      position: 'absolute',
      top: '20px',
      right: '20px',
      backgroundColor: '#222',
      color: 'white',
      padding: '10px',
      borderRadius: '8px',
      fontSize: '14px',
      zIndex: 1000
    }}>
      <label>
        <strong>Jahr:</strong>
        <select
          value={selectedYear}
          onChange={(e) => onChange(parseInt(e.target.value))}
          style={{ marginLeft: '8px', backgroundColor: '#333', color: 'white' }}
        >
          {years.map((year) => (
            <option key={year} value={year}>{year}</option>
          ))}
        </select>
      </label>
    </div>
  );
}

export default YearFilter;
