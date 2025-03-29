import React, { useState } from 'react';
import CrimeMap from './CrimeMap';
import Legend from './Legend';
import Filter from './Filter';

function App() {
  const [selectedTypes, setSelectedTypes] = useState([
    'Tötungsdelikt',
    'Messerstecherei',
    'Raubüberfall',
    'Vergewaltigung'
  ]);

  return (
    <>
      <CrimeMap selectedTypes={selectedTypes} />
      <Legend />
      <Filter selectedTypes={selectedTypes} onChange={setSelectedTypes} />
    </>
  );
}

export default App;
