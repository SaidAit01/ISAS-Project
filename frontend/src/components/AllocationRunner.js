import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ResultsTable from './ResultsTable';
import SystemSettings from './SystemSettings';

const AllocationRunner = () => {
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    // --- NEW: CAPACITY MANAGEMENT STATE ---
    const [supervisors, setSupervisors] = useState([]);
    const [loadingCapacity, setLoadingCapacity] = useState(false);

    // Fetch supervisors on component mount
    const fetchSupervisors = async () => {
        try {
            const res = await axios.get('http://127.0.0.1:8000/allocation/directory/');
            if (res.data.status === 'success') {
                setSupervisors(res.data.supervisors);
            }
        } catch (err) {
            console.error("Failed to load supervisors");
        }
    };

    useEffect(() => {
        fetchSupervisors();
    }, []);

    // Handle +/- capacity clicks
    const handleUpdateCapacity = async (supervisorId, currentCapacity, amount) => {
        const newCapacity = currentCapacity + amount;
        if (newCapacity < 0) return; // Prevent negative capacities

        setLoadingCapacity(true);
        try {
            const token = localStorage.getItem('access_token');
            await axios.post('http://127.0.0.1:8000/allocation/update-capacity/', 
                { id: supervisorId, capacity: newCapacity },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            
            // Refresh the table to show updated numbers
            fetchSupervisors(); 
        } catch (err) {
            alert("Failed to update capacity. Check your connection or permissions.");
        } finally {
            setLoadingCapacity(false);
        }
    };

    const runAlgorithm = async () => {
        setLoading(true);
        setError(null);

        try {
            const token = localStorage.getItem('access_token');

            const response = await axios.post(
                `http://127.0.0.1:8000/allocation/run-algo/`,
                {}, 
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );

            setResults(response.data);
        } catch (err) {
            console.error("FULL ENGINE ERROR:", err);
            const exactError = err.response?.data?.error || err.response?.data?.message || err.message || "Failed to connect.";
            setError(`Error: ${exactError}`);
        } finally {
            setLoading(false);
        }
    };

    const handleExport = async () => {
        try {
            const token = localStorage.getItem('access_token');

            const response = await axios.get('http://127.0.0.1:8000/allocation/export-csv/', {
                responseType: 'blob', 
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            
            link.setAttribute('download', 'final_allocations.csv');
            document.body.appendChild(link);
            link.click();

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
                <h2 className="fw-bold text-dark mb-0">⚙️ Project Coordinator Dashboard</h2>
            </div>

            {/* 1. THE GLOBAL SETTINGS PANEL */}
            <SystemSettings />

            {/* 2. THE CAPACITY MANAGEMENT PANEL (NEW) */}
            <div className="card shadow-sm mt-4 mb-4 border-0 border-top border-info border-4">
                <div className="card-header bg-white border-bottom pb-3 pt-4">
                    <h4 className="fw-bold text-info mb-1">👥 Supervisor Capacity Control</h4>
                    <p className="text-muted mb-0 small">Adjust the maximum number of students each academic can take before running the algorithm.</p>
                </div>
                <div className="card-body p-0">
                    <div className="table-responsive" style={{ maxHeight: "350px", overflowY: "auto" }}>
                        <table className="table table-hover align-middle mb-0">
                            <thead className="table-light sticky-top shadow-sm">
                                <tr>
                                    <th className="ps-4 py-3">Academic Name</th>
                                    <th className="text-center py-3">Current Limit</th>
                                    <th className="text-end pe-4 py-3">Adjust Allocation</th>
                                </tr>
                            </thead>
                            <tbody>
                                {supervisors.map((sup) => (
                                    <tr key={sup.id}>
                                        <td className="fw-bold text-dark ps-4">{sup.name}</td>
                                        <td className="text-center fs-5 text-primary fw-bold">
                                            {sup.capacity}
                                        </td>
                                        <td className="text-end pe-4">
                                            <button 
                                                className="btn btn-outline-danger btn-sm me-2 fw-bold px-3"
                                                onClick={() => handleUpdateCapacity(sup.id, sup.capacity, -1)}
                                                disabled={loadingCapacity || sup.capacity === 0}
                                            >
                                                - 1
                                            </button>
                                            <button 
                                                className="btn btn-outline-success btn-sm fw-bold px-3"
                                                onClick={() => handleUpdateCapacity(sup.id, sup.capacity, 1)}
                                                disabled={loadingCapacity}
                                            >
                                                + 1
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                                {supervisors.length === 0 && (
                                    <tr>
                                        <td colSpan="3" className="text-center text-muted py-4">Loading directory...</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            {/* 3. THE ALLOCATION ENGINE CONTROL */}
            <div className="card p-5 shadow-sm border-0 bg-white border-top border-primary border-4">
                <h3 className="fw-bold text-primary mb-2">🚀 Engine Control</h3>
                <p className="text-muted mb-4">Execute the SBERT Natural Language Processing and Gale-Shapley matching algorithm. This will overwrite any previous allocations in the database.</p>

                <div className="d-flex gap-3">
                    <button
                        className="btn btn-primary btn-lg fw-bold flex-grow-1 py-3"
                        onClick={runAlgorithm}
                        disabled={loading}
                    >
                        {loading ? "⚙️ Algorithm is running... please wait" : "Run Final Allocation"}
                    </button>

                    <button
                        className="btn btn-outline-success btn-lg fw-bold px-4 py-3"
                        onClick={handleExport}
                    >
                        📊 Download CSV
                    </button>
                </div>

                {error && <div className="alert alert-danger mt-4 fw-bold">{error}</div>}

                {/* 4. THE RESULTS TABLE */}
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