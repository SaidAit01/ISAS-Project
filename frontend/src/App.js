import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import StudentWizard from './components/StudentProposal';
import Navbar from './components/Navbar';
import Home from './components/Home';
import AllocationRunner from './components/AllocationRunner';
import SupervisorDashboard from './components/SupervisorDashboard';
import SupervisorDirectory from './components/SupervisorDirectory';
import StudentProposal from './components/StudentProposal';



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
            <Route path="/add-student" element={<StudentProposal />} />
            <Route path="/supervisor" element={<SupervisorDashboard />} />
            <Route path="/directory" element={<SupervisorDirectory />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;