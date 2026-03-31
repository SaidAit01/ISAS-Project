import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
    return (
        <div className="container mt-5 mb-5">
            {/* HERO SECTION */}
            <div className="p-5 bg-light rounded shadow-sm text-center mb-5 border-bottom border-primary border-4">
                <h1 className="display-4 fw-bold text-dark">Intelligent Student Allocation System</h1>
                <p className="lead text-muted mt-3">
                    A Hybrid Artificial Intelligence approach to solving the Student-Project Allocation problem.
                </p>
                <hr className="my-4" />
                <p>
                    Powered by <strong>Sentence-BERT Natural Language Processing</strong> and the mathematically stable <strong>Gale-Shapley Algorithm</strong>.
                </p>
            </div>

            {/* 2x2 USER JOURNEY GRID */}
            <div className="row g-4">

                {/* 1. THE DIRECTORY (NEW) */}
                <div className="col-md-6">
                    <div className="card h-100 shadow-sm border-0 bg-white">
                        <div className="card-body text-center p-5 d-flex flex-column">
                            <div className="display-6 mb-3">📚</div>
                            <h3 className="card-title text-dark fw-bold mb-3">Browse Supervisors</h3>
                            <p className="card-text text-muted mb-4">
                                Explore our full academic directory. View research interests, suggested project topics, and available supervision capacity before you start your proposal.
                            </p>
                            <Link className="btn btn-outline-dark fw-bold w-100 mt-auto py-2" to="/directory">
                                Open Directory →
                            </Link>
                        </div>
                    </div>
                </div>

                {/* 2. STUDENT Proposal */}
                <div className="col-md-6">
                    <div className="card h-100 shadow-sm border-0 bg-white">
                        <div className="card-body text-center p-5 d-flex flex-column">
                            <div className="display-6 mb-3">✨</div>
                            <h3 className="card-title text-primary fw-bold mb-3"> Student Proposal Portal</h3>
                            <p className="card-text text-muted mb-4">
                                Ready to submit? Use the Portal to describe your project idea and get instant matches with the most suitable academic supervisors based on a matching score calculated using our Engine.
                            </p>
                            <Link className="btn btn-primary fw-bold w-100 mt-auto py-2" to="/add-student">
                                Start Student Proposal
                            </Link>
                        </div>
                    </div>
                </div>

                {/* 3. SUPERVISOR PORTAL */}
                <div className="col-md-6">
                    <div className="card h-100 shadow-sm border-0 bg-white">
                        <div className="card-body text-center p-5 d-flex flex-column">
                            <div className="display-6 mb-3">👨‍🏫</div>
                            <h3 className="card-title text-info fw-bold mb-3">Supervisor Portal</h3>
                            <p className="card-text text-muted mb-4">
                                Academic staff can manage their profiles, update research interests, and view the students officially allocated to them for this academic year.
                            </p>
                            <Link className="btn btn-outline-info fw-bold w-100 mt-auto py-2" to="/supervisor">
                                Access Supervisor Portal
                            </Link>
                        </div>
                    </div>
                </div>

                {/* 4. ADMIN DASHBOARD */}
                <div className="col-md-6">
                    <div className="card h-100 shadow-sm border-0 bg-white">
                        <div className="card-body text-center p-5 d-flex flex-column">
                            <div className="display-6 mb-3">⚙️</div>
                            <h3 className="card-title text-success fw-bold mb-3">Module Leader Admin</h3>
                            <p className="card-text text-muted mb-4">
                                Central control for project administrators. Enforce capacity constraints, monitor pending submissions, and execute the final allocation engine.
                            </p>
                            <Link className="btn btn-success fw-bold w-100 mt-auto py-2" to="/allocation">
                                Allocation Dashboard
                            </Link>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Home;