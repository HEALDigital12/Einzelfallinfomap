import React, { useState } from 'react';
import CrimeMap from './CrimeMap';
import Legend from './Legend';
import Filter from './Filter';
import YearFilter from './YearFilter';
import LastUpdate from './LastUpdate';

function App() {
  const [selectedTypes, setSelectedTypes] = useState([
    'Tötung',
    'Messerstecherei',
    'Körperverletzung',
    'Sexualdelikt',
    'Raub'
  ]);
  const [selectedYear, setSelectedYear] = useState('2026');