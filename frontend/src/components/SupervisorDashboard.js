import React, { useState } from 'react';
import axios from 'axios';
import Select from 'react-select';
import CreatableSelect from 'react-select/creatable';

// --- TAXONOMY DEFINITIONS ---
const FORMAT_OPTIONS = [
    { value: 'Software Engineering', label: 'Software Engineering / System Development' },
    { value: 'Applied Research', label: 'Applied Research & AI' },
    { value: 'Data Science', label: 'Data Science & Analytics' },
    { value: 'Theoretical CS', label: 'Theoretical Computer Science' },
    { value: 'Hardware IoT', label: 'Hardware, IoT & Networking' },
    { value: 'HCI', label: 'Human-Computer Interaction (HCI)' }
];

const SKILL_OPTIONS = [
    { value: 'Python', label: 'Python' },
    { value: 'Java', label: 'Java' },
    { value: 'C++', label: 'C++' },
    { value: 'React', label: 'React' },
    { value: 'Node.js', label: 'Node.js' },
    { value: 'Docker', label: 'Docker' },
    { value: 'SQL', label: 'SQL' },
    { value: 'Machine Learning', label: 'Machine Learning' },
    { value: 'Data Analysis', label: 'Data Analysis' }
];

const INTEREST_OPTIONS = [
    { value: 'Artificial Intelligence', label: 'Artificial Intelligence' },
    { value: 'Cybersecurity', label: 'Cybersecurity' },
    { value: 'Web Development', label: 'Web Development' },
    { value: 'Cloud Computing', label: 'Cloud Computing' },
    { value: 'Computer Vision', label: 'Computer Vision' },
    { value: 'Robotics', label: 'Robotics' }
];

const SupervisorDashboard = () => {
    // --- AUTH / NAVIGATION STATE ---
    const [loginName, setLoginName] = useState("");
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [activeTab, setActiveTab] = useState("students");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [successMsg, setSuccessMsg] = useState("");

    // --- DATA STATE ---
    const [allocatedStudents, setAllocatedStudents] = useState([]);

    // --- PROFILE FORM STATE ---
    const [capacity, setCapacity] = useState(3);
    const [projects, setProjects] = useState(""); // Kept as text area based on your previous design
    
    // Updated to handle array objects for react-select
    const [selectedInterests, setSelectedInterests] = useState([]);
    const [selectedSkills, setSelectedSkills] = useState([]);
    const [selectedFormats, setSelectedFormats] = useState([]);

    // --- UI TOOLTIP STATE ---
    const [showFormatHelp, setShowFormatHelp] = useState(false);

    // --- LOGIC: ENTER PORTAL ---
    const handleLogin = async (e) => {
        e.preventDefault();
        if (!loginName.trim()) return;
        setLoading(true); setError(null);

        try {
            try {
                const profileRes = await axios.get(`http://127.0.0.1:8000/allocation/supervisor-profile/${encodeURIComponent(loginName)}/`);
                if (profileRes.data.status === 'success') {
                    const p = profileRes.data.profile;
                    setCapacity(p.capacity || 3);
                    setProjects(p.suggested_projects?.join(", ") || "");
                    
                    // Map existing DB string arrays back to react-select objects
                    setSelectedInterests(p.research_interests ? p.research_interests.map(i => ({value: i, label: i})) : []);
                    setSelectedSkills(p.technical_skills ? p.technical_skills.map(s => ({value: s, label: s})) : []);
                    setSelectedFormats(p.primary_project_format ? p.primary_project_format.map(f => ({value: f, label: f})) : []);
                }
            } catch (err) {
                setSuccessMsg("Welcome! It looks like you are a new supervisor. Please fill out your profile.");
                setActiveTab("profile"); 
            }

            try {
                const studentRes = await axios.get(`http://127.0.0.1:8000/allocation/my-students/${encodeURIComponent(loginName)}/`);
                if (studentRes.data.status === 'success') {
                    setAllocatedStudents(studentRes.data.students);
                }
            } catch (err) {
                setAllocatedStudents([]);
            }

            setIsLoggedIn(true);
        } catch (err) {
            setError("Failed to connect to the server.");
        } finally {
            setLoading(false);
        }
    };

    // --- LOGIC: SAVE PROFILE ---
    const handleSaveProfile = async (e) => {
        e.preventDefault();
        setLoading(true); setSuccessMsg(""); setError(null);

        // Map the react-select objects back to standard arrays and use the correct symmetric keys
        const payload = {
            name: loginName,
            capacity: parseInt(capacity),
            suggested_projects: projects.split(',').map(s => s.trim()).filter(s => s),
            research_interests: selectedInterests.map(i => i.value),
            technical_skills: selectedSkills.map(s => s.value),
            primary_project_format: selectedFormats.map(f => f.value),
        };

        try {
            const response = await axios.post('http://127.0.0.1:8000/allocation/add-supervisor/', payload);
            if (response.data.status === 'success') {
                setSuccessMsg(`Profile successfully saved! The AI engine now has your latest preferences.`);
            }
        } catch (err) {
            setError("Could not save profile. Check your connection.");
        } finally {
            setLoading(false);
        }
    };

    if (!isLoggedIn) {
        return (
            <div className="container mt-5 max-w-2xl mx-auto">
                <div className="card shadow-sm border-0 bg-light p-5 text-center">
                    <h2 className="text-dark fw-bold mb-3">👨‍🏫 Supervisor Portal</h2>
                    <p className="text-muted mb-4">Enter your full name to view your students or update your academic profile.</p>
                    <form onSubmit={handleLogin} className="d-flex justify-content-center">
                        <input
                            type="text"
                            className="form-control form-control-lg me-2 border-primary"
                            placeholder="e.g., Mariam Cirovic"
                            value={loginName} onChange={(e) => setLoginName(e.target.value)}
                        />
                        <button type="submit" className="btn btn-primary btn-lg fw-bold" disabled={loading}>
                            {loading ? "Loading..." : "Enter Portal"}
                        </button>
                    </form>
                </div>
            </div>
        );
    }

    return (
        <div className="container mt-4 max-w-4xl mx-auto">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h3 className="fw-bold">Welcome, <span className="text-primary">{loginName}</span></h3>
                <button className="btn btn-outline-danger btn-sm" onClick={() => setIsLoggedIn(false)}>Log Out</button>
            </div>

            <ul className="nav nav-tabs mb-4">
                <li className="nav-item">
                    <button className={`nav-link fw-bold ${activeTab === 'students' ? 'active text-primary' : 'text-muted'}`} onClick={() => setActiveTab('students')}>
                        🎓 My Allocated Students
                    </button>
                </li>
                <li className="nav-item">
                    <button className={`nav-link fw-bold ${activeTab === 'profile' ? 'active text-primary' : 'text-muted'}`} onClick={() => setActiveTab('profile')}>
                        ⚙️ Edit Profile & Settings
                    </button>
                </li>
            </ul>

            {successMsg && <div className="alert alert-success fw-bold">{successMsg}</div>}
            {error && <div className="alert alert-danger fw-bold">{error}</div>}

            {activeTab === 'students' && (
                <div>
                    {allocatedStudents.length === 0 ? (
                        <div className="alert alert-info text-center py-4 shadow-sm">
                            <h5 className="mb-0">You currently have no students allocated to you.</h5>
                        </div>
                    ) : (
                        <div className="row">
                            {allocatedStudents.map((student, idx) => (
                                <div className="col-md-6 mb-4" key={idx}>
                                    <div className="card h-100 shadow-sm border-success border-top border-4">
                                        <div className="card-body">
                                            <h4 className="card-title text-success fw-bold">{student.name}</h4>
                                            <p className="card-text text-dark">{student.topic}</p>
                                            <div className="mt-3">
                                                <span className="badge bg-secondary me-2 mb-2">🧠 {student.interests}</span>
                                                <span className="badge bg-info text-dark me-2 mb-2">💻 {student.languages}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {activeTab === 'profile' && (
                <div className="card shadow-sm p-4 border-0 bg-white">
                    <form onSubmit={handleSaveProfile}>
                        <div className="mb-4">
                            <label className="form-label fw-bold">Student Capacity Limit</label>
                            <input type="number" className="form-control w-25" value={capacity} onChange={(e) => setCapacity(e.target.value)} min="1" max="20" required />
                            <div className="form-text">Maximum number of final-year students you can supervise.</div>
                        </div>

                        <div className="row">
                            <div className="col-md-12 mb-3">
                                <label className="form-label fw-bold">Research Interests</label>
                                <CreatableSelect
                                    isMulti
                                    options={INTEREST_OPTIONS}
                                    value={selectedInterests}
                                    onChange={(opts) => setSelectedInterests(opts || [])}
                                    placeholder="Type an interest and press Enter..."
                                    formatCreateLabel={(val) => `Add "${val}"`}
                                />
                            </div>
                            
                            <div className="col-md-12 mb-3">
                                <label className="form-label fw-bold">Required Technical Skills</label>
                                <CreatableSelect
                                    isMulti
                                    options={SKILL_OPTIONS}
                                    value={selectedSkills}
                                    onChange={(opts) => setSelectedSkills(opts || [])}
                                    placeholder="Type a skill/language and press Enter..."
                                    formatCreateLabel={(val) => `Add "${val}"`}
                                />
                            </div>

                            <div className="col-md-12 mb-3">
                                <label className="form-label fw-bold d-flex align-items-center mb-2">
                                    Primary Project Format
                                    <span 
                                        className="badge bg-light text-secondary border border-secondary ms-2 rounded-1" 
                                        onClick={() => setShowFormatHelp(!showFormatHelp)}
                                        style={{ cursor: "pointer", fontSize: "0.8rem", padding: "0.4em 0.6em" }}
                                    >
                                        ?
                                    </span>
                                </label>

                                {showFormatHelp && (
                                    <div className="alert alert-secondary py-2 px-3 mb-3 shadow-sm" style={{ fontSize: "0.85rem" }}>
                                        <strong>System Matching Logic:</strong> Select the primary project modalities you are willing to supervise. The algorithm uses this as a strict filter to ensure you are matched with students whose projects align with your methodological grading expertise.
                                    </div>
                                )}

                                <Select
                                    isMulti
                                    options={FORMAT_OPTIONS}
                                    value={selectedFormats}
                                    onChange={(opts) => setSelectedFormats(opts || [])}
                                    placeholder="Select standard project formats..."
                                />
                            </div>

                            <div className="col-md-12 mb-4">
                                <label className="form-label fw-bold">Suggested Projects</label>
                                <textarea className="form-control" rows="3" value={projects} onChange={(e) => setProjects(e.target.value)} placeholder="e.g., Stock Prediction App, Database Engine"></textarea>
                                <div className="form-text">Note: Please separate multiple items with commas. This field is for student inspiration.</div>
                            </div>
                        </div>

                        <button type="submit" className="btn btn-success btn-lg w-100 fw-bold" disabled={loading}>
                            {loading ? "Saving..." : "💾 Save Supervisor Profile"}
                        </button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default SupervisorDashboard;