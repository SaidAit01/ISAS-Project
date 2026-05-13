import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select';
import CreatableSelect from 'react-select/creatable';

const SupervisorDashboard = () => {
    const [loginName, setLoginName] = useState("");
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [activeTab, setActiveTab] = useState("students");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [successMsg, setSuccessMsg] = useState("");
    const [allocatedStudents, setAllocatedStudents] = useState([]);

    const [capacity, setCapacity] = useState("");
    const [projects, setProjects] = useState(""); 
    
    const [selectedInterests, setSelectedInterests] = useState([]);
    const [selectedSkills, setSelectedSkills] = useState([]);
    const [selectedCategories, setSelectedCategories] = useState([]); 
    const [showCategoryHelp, setShowCategoryHelp] = useState(false); 

    const [categoryOptions, setCategoryOptions] = useState([]); 
    const [skillOptions, setSkillOptions] = useState([]);
    const [interestOptions, setInterestOptions] = useState([]);

    useEffect(() => {
        const fetchTaxonomies = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/allocation/taxonomies/');
                if (response.data.status === 'success') {
                    setCategoryOptions(response.data.categories.map(item => ({ value: item, label: item }))); 
                    setSkillOptions(response.data.skills.map(item => ({ value: item, label: item })));
                    setInterestOptions(response.data.interests.map(item => ({ value: item, label: item })));
                }
            } catch (error) {
                console.error("Could not fetch global taxonomies.", error);
            }
        };
        fetchTaxonomies();
    }, []);

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
                    
                    setSelectedInterests(p.research_interests ? p.research_interests.map(i => ({value: i, label: i})) : []);
                    setSelectedSkills(p.required_skills ? p.required_skills.map(s => ({value: s, label: s})) : []);
                    setSelectedCategories(p.project_category ? p.project_category.map(f => ({value: f, label: f})) : []); // FIXED
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

    const handleSaveProfile = async (e) => {
        e.preventDefault();
        setLoading(true); setSuccessMsg(""); setError(null);

        const payload = {
            name: loginName,
            suggested_projects: projects.split(',').map(s => s.trim()).filter(s => s),
            research_interests: selectedInterests.map(i => i.value),
            required_skills: selectedSkills.map(s => s.value),
            project_category: selectedCategories.map(f => f.value), // FIXED
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
                    <form onSubmit={handleLogin} className="d-flex justify-content-center mt-4">
                        <input type="text" className="form-control form-control-lg me-2 border-primary" placeholder="e.g., Mariam Cirovic" value={loginName} onChange={(e) => setLoginName(e.target.value)} />
                        <button type="submit" className="btn btn-primary btn-lg fw-bold" disabled={loading}>Enter Portal</button>
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
                    <button className={`nav-link fw-bold ${activeTab === 'students' ? 'active text-primary' : 'text-muted'}`} onClick={() => setActiveTab('students')}>🎓 My Allocated Students</button>
                </li>
                <li className="nav-item">
                    <button className={`nav-link fw-bold ${activeTab === 'profile' ? 'active text-primary' : 'text-muted'}`} onClick={() => setActiveTab('profile')}>⚙️ Edit Profile & Settings</button>
                </li>
            </ul>

            {successMsg && <div className="alert alert-success fw-bold">{successMsg}</div>}
            {error && <div className="alert alert-danger fw-bold">{error}</div>}

            {activeTab === 'students' && (
                <div>
                    {allocatedStudents.length === 0 ? (
                        <div className="alert alert-info text-center py-4 shadow-sm"><h5 className="mb-0">You currently have no students allocated to you.</h5></div>
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
                                                <span className="badge bg-info text-dark me-2 mb-2">💻 {student.skills}</span>
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
                            <label className="form-label fw-bold">Allocated Supervision Capacity</label>
                            <input type="number" className="form-control w-25 bg-light" value={capacity} disabled />
                        </div>

                        <div className="row">
                            <div className="col-md-12 mb-3">
                                <label className="form-label fw-bold">Research Interests</label>
                                <CreatableSelect isMulti options={interestOptions} value={selectedInterests} onChange={(opts) => setSelectedInterests(opts || [])} />
                            </div>
                            
                            <div className="col-md-12 mb-3">
                                <label className="form-label fw-bold">Required Technical Skills</label>
                                <CreatableSelect isMulti options={skillOptions} value={selectedSkills} onChange={(opts) => setSelectedSkills(opts || [])} />
                            </div>

                            <div className="col-md-12 mb-3">
                                <label className="form-label fw-bold d-flex align-items-center mb-2">
                                    Project Category
                                </label>
                                <Select isMulti options={categoryOptions} value={selectedCategories} onChange={(opts) => setSelectedCategories(opts || [])} />
                            </div>

                            <div className="col-md-12 mb-4">
                                <label className="form-label fw-bold">Suggested Projects</label>
                                <textarea className="form-control" rows="3" value={projects} onChange={(e) => setProjects(e.target.value)}></textarea>
                            </div>
                        </div>

                        <button type="submit" className="btn btn-success btn-lg w-100 fw-bold" disabled={loading}>💾 Save Supervisor Profile</button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default SupervisorDashboard;