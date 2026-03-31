import React, { useState } from 'react';
import axios from 'axios';
import ResultsTable from './ResultsTable';
import SystemSettings from './SystemSettings';

const AllocationRunner = () => {
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    const runAlgorithm = async () => {
        setLoading(true);
        setError(null);

        try {
            // CACHE-BUSTING TRICK: Adding ?t=... ensures the browser never caches this request!
            const timestamp = new Date().getTime();
            const response = await axios.get(`http://127.0.0.1:8000/allocation/run-algo/?t=${timestamp}`);

            setResults(response.data);
        } catch (err) {
            setError("Failed to connect to the Allocation Engine.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-4 max-w-5xl mx-auto mb-5">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2 className="fw-bold text-dark mb-0">⚙️ Module Leader Dashboard</h2>
            </div>

            {/* 1. THE GLOBAL SETTINGS PANEL */}
            <SystemSettings />

            {/* 2. THE ALLOCATION ENGINE CONTROL */}
            <div className="card p-5 shadow-sm border-0 bg-white border-top border-primary border-4">
                <h3 className="fw-bold text-primary mb-2">🚀 Engine Control</h3>
                <p className="text-muted mb-4">Execute the SBERT Natural Language Processing and Gale-Shapley matching algorithm. This will overwrite any previous allocations in the database.</p>

                <button
                    className="btn btn-primary btn-lg fw-bold w-100 py-3"
                    onClick={runAlgorithm}
                    disabled={loading}
                >
                    {loading ? "⚙️ Algorithm is running... please wait" : "Run Final Allocation"}
                </button>

                {error && <div className="alert alert-danger mt-4 fw-bold">{error}</div>}

                {/* 3. THE RESULTS TABLE */}
                {results && (
                    <div className="mt-5 animate-fade-in">
                        <div className="alert alert-success shadow-sm border-0 fw-bold">
                            ✅ Success! The algorithm has completed and matches have been saved to the database.
                        </div>

                        <ResultsTable
                            matched={results.matches?.matched || {}}
                            unallocated={results.matches?.unallocated || []}
                            pending={results.pending || []}
                        />
                    </div>
                )}
            </div>
        </div>
    );
};

export default AllocationRunner;