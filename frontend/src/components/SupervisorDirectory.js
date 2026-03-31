import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const SupervisorDirectory = () => {
    const [supervisors, setSupervisors] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchDirectory = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/allocation/directory/');
                if (response.data.status === 'success') {
                    setSupervisors(response.data.supervisors);
                }
            } catch (err) {
                setError("Failed to load the supervisor directory.");
            } finally {
                setLoading(false);
            }
        };
        fetchDirectory();
    }, []);

    // The Live Search Filter Logic
    const filteredSupervisors = supervisors.filter(sup => {
        const searchLower = searchTerm.toLowerCase();
        const matchName = sup.name.toLowerCase().includes(searchLower);
        const matchInterests = sup.interests.some(interest => interest.toLowerCase().includes(searchLower));
        return matchName || matchInterests;
    });

    return (
        <div className="container mt-5 mb-5">
            <div className="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
                <div>
                    <h2 className="fw-bold text-dark mb-1">📚 Academic Staff Directory</h2>
                    <p className="text-muted mb-0">Browse available supervisors and their research interests.</p>
                </div>
                <Link to="/add-student" className="btn btn-primary fw-bold">
                    ✨ Submit your Proposal
                </Link>
            </div>

            {/* LIVE SEARCH BAR */}
            <div className="row mb-5">
                <div className="col-md-6 mx-auto">
                    <input
                        type="text"
                        className="form-control form-control-lg shadow-sm border-primary"
                        placeholder="🔍 Search by name or research interest (e.g., 'React', 'AI')..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>

            {loading && <div className="text-center mt-5"><div className="spinner-border text-primary" role="status"></div></div>}
            {error && <div className="alert alert-danger text-center fw-bold">{error}</div>}

            {/* SUPERVISOR GRID */}
            {!loading && !error && (
                <div className="row g-4">
                    {filteredSupervisors.length === 0 ? (
                        <div className="col-12 text-center text-muted mt-4">
                            <h5>No supervisors found matching "{searchTerm}"</h5>
                        </div>
                    ) : (
                        filteredSupervisors.map((sup) => (
                            <div className="col-md-4" key={sup.id}>
                                <div className="card h-100 shadow-sm border-0 border-top border-info border-4 hover-shadow">
                                    <div className="card-body">
                                        <h4 className="card-title fw-bold text-dark mb-3">{sup.name}</h4>

                                        <div className="mb-3">
                                            <h6 className="text-muted small text-uppercase fw-bold mb-2">Research Interests</h6>
                                            {sup.interests.length > 0 ? (
                                                sup.interests.map((interest, i) => (
                                                    <span key={i} className="badge bg-light text-dark border me-1 mb-1">{interest}</span>
                                                ))
                                            ) : (
                                                <span className="text-muted small">Not specified</span>
                                            )}
                                        </div>

                                        {sup.suggested_projects.length > 0 && (
                                            <div className="mb-3">
                                                <h6 className="text-muted small text-uppercase fw-bold mb-1">Suggested Projects</h6>
                                                <ul className="small text-dark ps-3 mb-0">
                                                    {sup.suggested_projects.map((proj, i) => (
                                                        <li key={i}>{proj}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                        )}
                                    </div>
                                    <div className="card-footer bg-white border-0 text-end">
                                        <span className="text-muted small">Capacity: <strong>{sup.capacity}</strong> students</span>
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            )}
        </div>
    );
};

export default SupervisorDirectory;