import React from 'react';
import { Link } from 'react-router-dom'; // 'Link' replaces HTML <a> tags

const Navbar = () => {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark mb-4 shadow-sm">
            <div className="container">
                <Link className="navbar-brand fw-bold" to="/">ISAS System</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav ms-auto">
                        <li className="nav-item">
                            <Link className="nav-link" to="/">Home</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to="/allocation">Allocation Dashboard</Link>
                        </li>

                        <li className="nav-item">
                            <Link className="nav-link text-warning fw-bold" to="/add-student"> Student Proposal Submission</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to="/supervisor">Supervisor Portal</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to="/directory">Browse Supervisors</Link>
                        </li>

                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;