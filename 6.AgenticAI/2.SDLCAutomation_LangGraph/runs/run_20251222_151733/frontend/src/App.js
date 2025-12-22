import React, { useEffect, useState } from 'react';

function App() {
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8080/patients')
      .then(response => response.json())
      .then(data => setPatients(data));
  }, []);

  return (
    <div>
      <h1>Patient Management</h1>
      <ul>
        {patients.map(patient => (
          <li key={patient.id}>{patient.name} - Age: {patient.age}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;