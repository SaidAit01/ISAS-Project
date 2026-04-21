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
            // 1. Grab the token from the browser vault
            const token = localStorage.getItem('access_token');

            // 2. Explicitly attach the token to the POST request headers
            const response = await axios.post(
                `http://127.0.0.1:8000/allocation/run-algo/`,
                {}, // Empty data payload
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );

            setResults(response.data);
        } catch (err) {
            console.error("FULL ENGINE ERROR:", err);
            // Try to extract the exact error message from Django
            const exactError = err.response?.data?.error || err.response?.data?.message || err.message || "Failed to connect.";
            setError(`Error: ${exactError}`);
        } finally {
            setLoading(false);
        }
    };

    const handleExport = async () => {
        try {
            // Grab the token here as well to be completely safe
            const token = localStorage.getItem('access_token');

            // Fetch the CSV using Axios and explicitly attach the token
            const response = await axios.get('http://127.0.0.1:8000/allocation/export-csv/', {
                responseType: 'blob', 
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            // Create a temporary ghost link in the browser memory
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            
            // Name the file and force the browser to click it
            link.setAttribute('download', 'final_allocations.csv');
            document.body.appendChild(link);
            link.click();

            // Clean up the ghost link
            link.parentNode.removeChild(link);
            window.URL.revokeObjectURL(url);
            
        } catch (err) {
            console.error("Failed to download CSV:", err);
            setError("Could not download the CSV file. You might lack permissions.");
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

                <button
                    className="btn btn-outline-success btn-lg fw-bold ms-2 px-4"
                    onClick={handleExport}
                >
                    📊 Download CSV for Registry
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