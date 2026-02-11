import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import AllocationRunner from './components/AllocationRunner'; // <--- IMPORT IT

function App() {
  return (
    <div className="container mt-5">
      <h1 className="mb-4">ISAS Dashboard</h1>
      
      {/* PLACE THE COMPONENT HERE */}
      <AllocationRunner /> 
      
    </div>
  );
}

export default App;