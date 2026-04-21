import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
    const navigate = useNavigate();
    
    // Check if the user is currently logged in
    const token = localStorage.getItem('access_token');

    // Handle the logout process
    const handleLogout = () => {
        localStorage.removeItem('access_token');
        navigate('/login');
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark mb-4 shadow-sm">
            <div className="container">
                <Link className="navbar-brand fw-bold" to="/">ISAS System</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav ms-auto align-items-center">
                        <li className="nav-item">
                            <Link className="nav-link" to="/">Home</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to="/allocation">Allocation Dashboard</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to="/add-student"> Student Proposal</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to="/supervisor">Supervisor Portal</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to="/directory">Browse Supervisors</Link>
                        </li>

                        {/* --- THE DYNAMIC AUTH BUTTON --- */}
                        {token ? (
                            <li className="nav-item ms-3">
                                <button onClick={handleLogout} className="btn btn-outline-danger btn-sm fw-bold">
                                    Log Out
                                </button>
                            </li>
                        ) : (
                            <li className="nav-item ms-3">
                                <Link className="btn btn-primary btn-sm fw-bold px-4" to="/login">
                                    Log In
                                </Link>
                            </li>
                        )}
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;