import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DataEntry = () => {
    // 1. Form State
    const [name, setName] = useState('');
    const [topic, setTopic] = useState('');
    const [pref, setPref] = useState('');
    const [message, setMessage] = useState('');
    
    // 2. The Global Rule State (Default is 3)
    const [maxPrefs, setMaxPrefs] = useState(3);

    const wordCount = topic.trim() === '' ? 0 : topic.trim().split(/\s+/).length;


    // 3. The Side Effect (Fetching the Module Leader's rule on load)
    useEffect(() => {
        const fetchConfig = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/allocation/get-config/');
                if (response.data.status === 'success') {
                    setMaxPrefs(response.data.max_preferences);
                }
            } catch (error) {
                console.error("Could not fetch system rules.", error);
            }
        };
        
        fetchConfig(); // Call the function immediately
    }, []); // Empty array means "Only run this once when the page loads"

    const handleSubmit = async (e) => {
        e.preventDefault(); // Stop page refresh
        setMessage('Sending...');
        if (wordCount > 200) {
            setMessage(`Hold on! Your topic description is too long. Please limit it to 200 words (currently ${wordCount} words).`);
            return; // Stop execution
        }
        if (wordCount < 50) {
            setMessage(`Hold on! Your topic description is too short. Please provide at least 50 words (currently ${wordCount} words).`);
            return; // Stop execution
        }
        try {
            // Clean up the input string into a proper array
            const preferencesArray = pref.split(',').map(s => s.trim()).filter(s => s);

            // FRONTEND BOUNCER: Stop them before they even bother Django
            if (preferencesArray.length > maxPrefs) {
                setMessage(`Wait! The Module Leader has restricted you to a maximum of ${maxPrefs} choices.`);
                return; // Stop execution
            }

            const payload = {
                name: name,
                topic: topic,
                preferences: preferencesArray
            };

            // Send to Django
            const response = await axios.post('http://127.0.0.1:8000/allocation/add-student/', payload);
            
            setMessage(`Success! Added student: ${name}`);
            setName('');
            setTopic('');
            setPref('');
        } catch (error) {
            // Show the strict error message from Django if it fails
            const errorMsg = error.response?.data?.message || 'Error: Could not add student.';
            setMessage(errorMsg);
        }
    };

    return (
        <div className="card p-4 shadow-sm mt-4">
            <h3>Add New Student Proposal</h3>
            
            {/* Dynamic UI Rule Display */}
            <div className="alert alert-warning">
                <strong>Current Department Policy:</strong> Students may select a maximum of <strong>{maxPrefs}</strong> preferred supervisors.
            </div>

            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Student Name</label>
                    <input type="text" className="form-control" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
                
                <div className="mb-3">
                    <label className="form-label">Research Topic</label>
                    <textarea className="form-control" rows="3" value={topic} onChange={(e) => setTopic(e.target.value)} required></textarea>
                </div>
                <div className={`form-text ${wordCount > 200 ? 'text-danger fw-bold' : 'text-muted'}`}>
                    Words: {wordCount} / 200
                </div>

                <div className="mb-3">
                    <label className="form-label">Manual Preferences (Comma separated)</label>
                    <input 
                        type="text" 
                        className="form-control" 
                        placeholder="Dr. Web, Dr. AI" 
                        value={pref} 
                        onChange={(e) => setPref(e.target.value)} 
                    />
                    <div className="form-text text-danger">
                        You may only enter up to {maxPrefs} names.
                    </div>
                </div>

                <button type="submit" className="btn btn-success">Submit Proposal</button>
            </form>

            {message && <div className="alert alert-info mt-3">{message}</div>}
        </div>
    );
};

export default DataEntry;