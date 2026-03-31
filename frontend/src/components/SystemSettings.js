import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SystemSettings = () => {
    const [maxPreferences, setMaxPreferences] = useState(3);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);
    const [error, setError] = useState(null);

    // Fetch the current rule when the dashboard loads
    useEffect(() => {
        const fetchSettings = async () => {
            try {
                // IMPORTANT: Ensure this URL matches your urls.py exactly!
                const response = await axios.get('http://127.0.0.1:8000/allocation/config/');
                if (response.data.status === 'success') {
                    setMaxPreferences(response.data.max_preferences);
                }
            } catch (err) {
                console.error("Could not load system settings.");
            }
        };
        fetchSettings();
    }, []);

    // Save the new rule to the database
    const handleSave = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage(null);
        setError(null);

        try {
            const response = await axios.post('http://127.0.0.1:8000/allocation/config/', {
                max_preferences: maxPreferences
            });

            if (response.data.status === 'success') {
                setMessage(response.data.message);
                // Clear the success message after 4 seconds so it doesn't clutter the screen
                setTimeout(() => setMessage(null), 4000);
            }
        } catch (err) {
            setError(err.response?.data?.message || "Failed to update global settings.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card shadow-sm border-0 border-start border-warning border-4 mb-4 bg-white">
            <div className="card-body p-4">
                <div className="d-flex align-items-center justify-content-between mb-3">
                    <div>
                        <h4 className="card-title text-dark fw-bold mb-1">⚙️ Global System Rules</h4>
                        <p className="text-muted small mb-0">Adjust constraints before running the allocation algorithm.</p>
                    </div>
                </div>

                {message && <div className="alert alert-success py-2 fw-bold">{message}</div>}
                {error && <div className="alert alert-danger py-2 fw-bold">{error}</div>}

                <form onSubmit={handleSave} className="d-flex align-items-end bg-light p-3 rounded">
                    <div className="flex-grow-1 me-3">
                        <label className="form-label fw-bold text-dark mb-1">Maximum Supervisor Preferences</label>
                        <input
                            type="number"
                            className="form-control border-warning"
                            value={maxPreferences}
                            onChange={(e) => setMaxPreferences(e.target.value)}
                            min="1"
                            max="10"
                            required
                        />
                        <div className="form-text mt-1">
                            The number of choices a student can make in the AI Proposal Wizard.
                        </div>
                    </div>
                    <button type="submit" className="btn btn-warning fw-bold text-dark px-4" disabled={loading}>
                        {loading ? "Saving..." : "Apply Rule"}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default SystemSettings;