import React, { useState } from 'react';
import axios from 'axios';

const SupervisorDashboard = () => {
    // --- AUTH / NAVIGATION STATE ---
    const [loginName, setLoginName] = useState("");
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [activeTab, setActiveTab] = useState("students"); // 'students' or 'profile'
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [successMsg, setSuccessMsg] = useState("");

    // --- DATA STATE ---
    const [allocatedStudents, setAllocatedStudents] = useState([]);

    // --- PROFILE FORM STATE ---
    const [capacity, setCapacity] = useState(3);
    const [interests, setInterests] = useState("");
    const [projects, setProjects] = useState("");
    const [skills, setSkills] = useState("");
    const [categories, setCategories] = useState("");

    // --- LOGIC: ENTER PORTAL ---
    const handleLogin = async (e) => {
        e.preventDefault();
        if (!loginName.trim()) return;
        setLoading(true); setError(null);

        try {
            // 1. Try to fetch their profile
            try {
                const profileRes = await axios.get(`http://127.0.0.1:8000/allocation/supervisor-profile/${encodeURIComponent(loginName)}/`);
                if (profileRes.data.status === 'success') {
                    const p = profileRes.data.profile;
                    // Pre-fill the form with their existing database info!
                    setCapacity(p.capacity);
                    setInterests(p.research_interests.join(", "));
                    setProjects(p.suggested_projects?.join(", ") || "");
                    setSkills(p.required_skills?.join(", ") || "");
                    setCategories(p.project_categories?.join(", ") || "");
                }
            } catch (err) {
                // If it 404s, it means they are a NEW supervisor. We just leave the form blank.
                setSuccessMsg("Welcome! It looks like you are a new supervisor. Please fill out your profile.");
                setActiveTab("profile"); // Force them to the profile tab
            }

            // 2. Fetch their students (if any)
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

        // Convert the comma-separated text into neat arrays for Django's JSON fields
        const payload = {
            name: loginName,
            capacity: parseInt(capacity),
            research_interests: interests.split(',').map(s => s.trim()).filter(s => s),
            suggested_projects: projects.split(',').map(s => s.trim()).filter(s => s),
            required_skills: skills.split(',').map(s => s.trim()).filter(s => s),
            project_categories: categories.split(',').map(s => s.trim()).filter(s => s),
        };

        try {
            const response = await axios.post('http://127.0.0.1:8000/allocation/add-supervisor/', payload);
            if (response.data.status === 'success') {
                setSuccessMsg(`Profile successfully ${response.data.action}! The AI engine now has your latest preferences.`);
            }
        } catch (err) {
            setError("Could not save profile. Check your connection.");
        } finally {
            setLoading(false);
        }
    };

    // ==========================================
    // UI: LOGIN SCREEN
    // ==========================================
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

    // ==========================================
    // UI: LOGGED IN DASHBOARD
    // ==========================================
    return (
        <div className="container mt-4 max-w-4xl mx-auto">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h3 className="fw-bold">Welcome, <span className="text-primary">{loginName}</span></h3>
                <button className="btn btn-outline-danger btn-sm" onClick={() => setIsLoggedIn(false)}>Log Out</button>
            </div>

            {/* TAB NAVIGATION */}
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

            {/* TAB 1: VIEW STUDENTS */}
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

            {/* TAB 2: EDIT PROFILE */}
            {activeTab === 'profile' && (
                <div className="card shadow-sm p-4 border-0 bg-white">
                    <form onSubmit={handleSaveProfile}>
                        <div className="mb-4">
                            <label className="form-label fw-bold">Student Capacity Limit</label>
                            <input type="number" className="form-control w-25" value={capacity} onChange={(e) => setCapacity(e.target.value)} min="1" max="20" required />
                            <div className="form-text">Maximum number of final-year students you can supervise.</div>
                        </div>

                        <div className="row">
                            <div className="col-md-6 mb-3">
                                <label className="form-label fw-bold">Research Interests</label>
                                <textarea className="form-control" rows="3" value={interests} onChange={(e) => setInterests(e.target.value)} placeholder="e.g., AI, Databases, Cloud Computing"></textarea>
                            </div>
                            <div className="col-md-6 mb-3">
                                <label className="form-label fw-bold">Required Skills</label>
                                <textarea className="form-control" rows="3" value={skills} onChange={(e) => setSkills(e.target.value)} placeholder="e.g., Python, SQL, React"></textarea>
                            </div>
                            <div className="col-md-6 mb-3">
                                <label className="form-label fw-bold">Suggested Projects</label>
                                <textarea className="form-control" rows="3" value={projects} onChange={(e) => setProjects(e.target.value)} placeholder="e.g., Stock Prediction App, Database Engine"></textarea>
                            </div>
                            <div className="col-md-6 mb-3">
                                <label className="form-label fw-bold">Project Categories</label>
                                <textarea className="form-control" rows="3" value={categories} onChange={(e) => setCategories(e.target.value)} placeholder="e.g., Web App, Research, Machine Learning"></textarea>
                            </div>
                        </div>
                        <div className="form-text mb-4 text-primary fw-bold">Note: Please separate multiple items with commas. Our system will format it automatically.</div>

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