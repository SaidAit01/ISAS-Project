import React, { useState } from 'react';
import axios from 'axios'; // The tool used to talk to Django

const AllocationRunner = () => {
    // --- STATE MANAGEMENT (The Memory) ---
    // 1. loading: Are we waiting for Django? (True/False)
    const [loading, setLoading] = useState(false);
    // 2. results: The JSON data from Django. (Starts empty)
    const [results, setResults] = useState(null);
    // 3. error: Did something break?
    const [error, setError] = useState(null);

    // --- THE FUNCTION (The Action) ---
    const runAlgorithm = async () => {
        setLoading(true); // Tell React: "We are busy, show a spinner"
        setError(null);   // Clear old errors

        try {
            // This is the specific URL for your Django View
            const response = await axios.get('http://127.0.0.1:8000/allocation/run-algo/');
            
            // If successful, save the data to Memory
            setResults(response.data); 
        } catch (err) {
            setError("Failed to connect to the Allocation Engine.");
            console.error(err);
        } finally {
            setLoading(false); // We are done, stop spinning
        }
    };

    // --- THE RENDER (The UI) ---
    return (
        <div className="card p-4 shadow-sm">
            <h3>Allocation Control</h3>
            <p>Click below to trigger the SPA + AI Algorithm.</p>
            
            <button 
                className="btn btn-primary" 
                onClick={runAlgorithm} 
                disabled={loading} // Disable button if busy
            >
                {loading ? "Running AI..." : "Run Allocation"}
            </button>

            {/* CONDITIONAL RENDERING: Only show error if error exists */}
            {error && <div className="alert alert-danger mt-3">{error}</div>}

            {/* Only show results if results exist */}
            {results && (
                <div className="mt-4">
                    <div className="alert alert-success">
                        <strong>Status:</strong> {results.status}
                    </div>
                    {/* We will display the full table later. For now, just dump the text */}
                    <pre>{JSON.stringify(results.matches, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default AllocationRunner;