import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

// Components
import Navbar from './components/Navbar';
import Home from './components/Home';
import AllocationRunner from './components/AllocationRunner';
import SupervisorDashboard from './components/SupervisorDashboard';
import SupervisorDirectory from './components/SupervisorDirectory';
import StudentProposal from './components/StudentProposal';
import ProtectedRoute from './components/ProtectedRoute'; 
import Login from './components/Login';

function App() {
  return (
    <Router>
      <div className="App">
        {/* The Navbar stays visible on ALL pages */}
        <Navbar />

        <div className="container">
          {/* The Routes determine what gets loaded in the main area */}
          <Routes>
            {/* --- PUBLIC ROUTES --- */}
            <Route path="/" element={<Home />} />
            
            {/* Fallback route for users trying to access the wrong dashboard */}
            
            <Route path="/unauthorised" element={
              <div className="alert alert-danger mt-5 text-center fw-bold">
                🚫 You do not have permission to view this page.
              </div>
            } />

           <Route path="/login" element={<Login />} />

            {/* --- PROTECTED ROUTES --- */}
            
            {/* 1. Project Coordinator Only */}
            <Route 
              path="/allocation" 
              element={
                <ProtectedRoute allowedRoles={['Project_Coordinator']}>
                  <AllocationRunner />
                </ProtectedRoute>
              } 
            />

            {/* 2. Student Only */}
            <Route 
              path="/add-student" 
              element={
                <ProtectedRoute allowedRoles={['Student']}>
                  <StudentProposal />
                </ProtectedRoute>
              } 
            />

            {/* 3. Supervisor Only */}
            <Route 
              path="/supervisor" 
              element={
                <ProtectedRoute allowedRoles={['Supervisor']}>
                  <SupervisorDashboard />
                </ProtectedRoute>
              } 
            />

            {/* 4. Directory (Available to all logged-in users) */}
            <Route 
              path="/directory" 
              element={
                <ProtectedRoute allowedRoles={['Student', 'Supervisor', 'Project_Coordinator']}>
                  <SupervisorDirectory />
                </ProtectedRoute>
              } 
            />

          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;