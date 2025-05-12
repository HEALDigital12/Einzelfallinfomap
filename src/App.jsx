import React, { useState, useEffect } from 'react';
import CrimeMap from './CrimeMap';
import Legend from './Legend';
import Filter from './Filter';
import YearFilter from './YearFilter';
import LastUpdate from './LastUpdate';

function App() {
  const [selectedTypes, setSelectedTypes] = useState([
    'Tötung',
    'Messerstecherei',
    'Raub',
    'Sexualdelikt'
    // Hier sind die initial ausgewählten schweren Straftaten
  ]);
  const [selectedYear, setSelectedYear] = useState(2025);

  // Optional: Initialisiere ausgewählte Typen nach dem Mounten
  useEffect(() => {
    setSelectedTypes(['Tötung', 'Messerstecherei', 'Raub', 'Sexualdelikt']);
  }, []);

  return (
    <>
      <CrimeMap selectedTypes={selectedTypes} selectedYear={selectedYear} />
      <Legend />
      <Filter selectedTypes={selectedTypes} onChange={setSelectedTypes} />
      <YearFilter selectedYear={selectedYear} onChange={setSelectedYear} />
      <LastUpdate />
    </>
  );
}

export default App;
import React, { useState } from 'react';
import CrimeMap from './CrimeMap';
import Legend from './Legend';
import Filter from './Filter';
import YearFilter from './YearFilter';
import LastUpdate from './LastUpdate';

function App() {
  const [selectedTypes, setSelectedTypes] = useState([
    'Verkehrsunfall',
    'Einbruch'
    // Füge hier weitere Delikttypen hinzu, die in deiner JSON vorkommen.
  ]);
  const [selectedYear, setSelectedYear] = useState(2025);

  return (
    <>
      <CrimeMap selectedTypes={selectedTypes} selectedYear={selectedYear} />
      <Legend />
      <Filter selectedTypes={selectedTypes} onChange={setSelectedTypes} />
      <YearFilter selectedYear={selectedYear} onChange={setSelectedYear} />
      <LastUpdate />
    </>
  );
}

export default App;
