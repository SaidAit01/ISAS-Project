import React from 'react';
import { Link } from 'react-router-dom'; // 'Link' replaces HTML <a> tags

const Navbar = () => {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
            <div className="container">
                <Link className="navbar-brand" to="/">ISAS System</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav ms-auto">
                        <li className="nav-item">
                            <Link className="nav-link" to="/">Home</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to="/allocation">Run Algorithm</Link>
                        </li>
                        <li className="nav-item">
                            {/* We will build this page later */}
                            <span className="nav-link disabled">Data Entry (Coming Soon)</span>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;