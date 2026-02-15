import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

// Import our Lego Bricks
import Navbar from './components/Navbar';
import Home from './components/Home';
import AllocationRunner from './components/AllocationRunner';

function App() {
  return (
    <Router>
      <div className="App">
        {/* The Navbar stays visible on ALL pages */}
        <Navbar />

        <div className="container">
          {/* The Routes determine what gets loaded in the main area */}
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/allocation" element={<AllocationRunner />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;