import React, { useState } from 'react';
import axios from 'axios';
import ResultsTable from './ResultsTable';

const AllocationRunner = () => {
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    const runAlgorithm = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await axios.get('http://127.0.0.1:8000/allocation/run-algo/');
            setResults(response.data);
        } catch (err) {
            setError("Failed to connect to the Allocation Engine.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card p-4 shadow-sm">
            <h3>Allocation Control</h3>
            <p>Click below to trigger the SPA + AI Algorithm.</p>

            <button
                className="btn btn-primary"
                onClick={runAlgorithm}
                disabled={loading}
            >
                {loading ? "Running AI..." : "Run Allocation"}
            </button>

            {error && <div className="alert alert-danger mt-3">{error}</div>}

            {results && (
                <div className="mt-4">
                    <div className="alert alert-success">
                        <strong>Status:</strong> {results.status}
                    </div>
                    {/* CRITICAL FIX: Pass the nested data as two separate props */}
                    <ResultsTable
                        matched={results.matches?.matched || {}}
                        unallocated={results.matches?.unallocated || []}
                        pending={results.pending || []}
                    />
                </div>
            )}
        </div>
    );
};

export default AllocationRunner;