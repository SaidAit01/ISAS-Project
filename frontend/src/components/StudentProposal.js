import React, { useState, useEffect } from 'react';
import axios from 'axios';

const StudentProposal = () => {

    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');

    // --- 2. THE GLOBAL RULE STATE ---
    const [maxPrefs, setMaxPrefs] = useState(3);

    // --- 3. FORM DATA STATE ---
    const [name, setName] = useState("");
    const [topic, setTopic] = useState("");
    const [interestsInput, setInterestsInput] = useState("");
    const [languagesInput, setLanguagesInput] = useState("");
    const [categoryInput, setCategoryInput] = useState("");
    const [finalPrefs, setFinalPrefs] = useState("");

    // --- 4. NEW: PRE-AGREEMENT STATE ---
    const [hasPreAgreement, setHasPreAgreement] = useState(false);
    const [selectedSupervisor, setSelectedSupervisor] = useState("");
    const [supervisorList, setSupervisorList] = useState([]);

    // --- 5. AI RESULTS STATE ---
    const [suggestions, setSuggestions] = useState([]);

    const wordCount = topic.trim() === '' ? 0 : topic.trim().split(/\s+/).length;

    useEffect(() => {
        // Fetch global rules
        const fetchConfig = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/allocation/config/');
                if (response.data.status === 'success') {
                    setMaxPrefs(response.data.max_preferences);
                }
            } catch (error) {
                console.error("Could not fetch system rules.", error);
            }
        };

        // Fetch staff directory for the dropdown
        const fetchSupervisors = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/allocation/directory/');
                if (response.data.status === 'success') {
                    setSupervisorList(response.data.supervisors);
                }
            } catch (error) {
                console.error("Could not fetch supervisor directory.", error);
            }
        };

        fetchConfig();
        fetchSupervisors();
    }, []);

    // --- ACTION 1: Get AI Suggestions (Standard Route) ---
    const handleGetSuggestions = async () => {
        setError(null);

        if (wordCount > 200) return setError(`Topic is too long. Limit: 200 words (currently ${wordCount}).`);
        if (!topic.trim() && !interestsInput.trim() && !languagesInput.trim() && !categoryInput.trim()) {
            return setError("Please provide a topic description or fill in some of the skills/category fields.");
        }

        setLoading(true);

        try {
            const combinedKeywords = [
                ...interestsInput.split(','),
                ...languagesInput.split(','),
                ...categoryInput.split(',')
            ].map(item => item.trim()).filter(item => item !== "");

            const response = await axios.post('http://127.0.0.1:8000/allocation/suggest-supervisors/', {
                topic: topic,
                interests: combinedKeywords
            });

            if (response.data.status === 'success') {
                setSuggestions(response.data.suggestions);
                setStep(2);
            }
        } catch (err) {
            setError(err.response?.data?.message || "Failed to connect to the AI Engine.");
        } finally {
            setLoading(false);
        }
    };

    // --- ACTION 2: Fast-Track Submit (Pre-Agreement Route) ---
    const handleSubmitPreAgreement = async (e) => {
        e.preventDefault();
        setError(null);

        if (wordCount > 200) return setError(`Topic is too long. Limit: 200 words.`);
        if (!selectedSupervisor) return setError("Please select your pre-agreed supervisor from the list.");

        setLoading(true);
        try {
            const payload = {
                name: name,
                topic: topic,
                interests: interestsInput.split(',').map(s => s.trim()).filter(s => s),
                programming_languages: languagesInput.split(',').map(s => s.trim()).filter(s => s),
                project_category: categoryInput.split(',').map(s => s.trim()).filter(s => s),
                preferences: [], // No manual prefs needed!
                has_pre_agreement: true,
                pre_agreed_supervisor: selectedSupervisor
            };

            await axios.post('http://127.0.0.1:8000/allocation/add-student/', payload);

            setSuccessMessage(`Success! Your pre-agreement with ${selectedSupervisor} has been officially recorded. You will bypass the matching algorithm.`);
            setStep(3); // Go straight to the finish line!
        } catch (err) {
            setError(err.response?.data?.message || 'Error: Could not add student.');
        } finally {
            setLoading(false);
        }
    };

    // --- ACTION 3: Final Submission (Standard Route) ---
    const handleFinalSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        try {
            const preferencesArray = finalPrefs.split(',').map(s => s.trim()).filter(s => s);

            if (preferencesArray.length > maxPrefs) {
                setLoading(false);
                return setError(`The Module Leader strictly limits you to a maximum of ${maxPrefs} choices.`);
            }

            const payload = {
                name: name,
                topic: topic,
                interests: interestsInput.split(',').map(s => s.trim()).filter(s => s),
                programming_languages: languagesInput.split(',').map(s => s.trim()).filter(s => s),
                project_category: categoryInput.split(',').map(s => s.trim()).filter(s => s),
                preferences: preferencesArray,
                has_pre_agreement: false, // Standard route
                pre_agreed_supervisor: ""
            };

            await axios.post('http://127.0.0.1:8000/allocation/add-student/', payload);

            setSuccessMessage(`Success! Proposal for ${name} has been officially recorded and moved to the active matching pool.`);
            setStep(3);
        } catch (error) {
            setError(error.response?.data?.message || 'Error: Could not add student.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card p-4 shadow-sm mt-4 max-w-3xl mx-auto">
            <h3 className="border-bottom pb-2 mb-4">Student Proposal</h3>

            <div className="alert alert-warning mb-4">
                <strong>Department Policy:</strong> You may select a maximum of <strong>{maxPrefs}</strong> preferred supervisors unless you have a pre-agreement.
            </div>

            {error && <div className="alert alert-danger fw-bold">{error}</div>}

            {step === 1 && (
                <div>
                    <div className="mb-3">
                        <label className="form-label fw-bold">Full Name</label>
                        <input type="text" className="form-control" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g., Ada Lovelace" required />
                    </div>

                    <div className="mb-1">
                        <label className="form-label fw-bold">Project Topic Description</label>
                        <textarea className="form-control" rows="4" value={topic} onChange={(e) => setTopic(e.target.value)} placeholder="Describe your project idea..."></textarea>
                    </div>
                    <div className={`form-text mb-3 ${wordCount > 200 ? 'text-danger fw-bold' : 'text-muted'}`}>
                        Words: {wordCount} / 200 Maximum
                    </div>

                    <div className="row">
                        <div className="col-md-4 mb-3">
                            <label className="form-label fw-bold">Research Interests</label>
                            <input type="text" className="form-control" value={interestsInput} onChange={(e) => setInterestsInput(e.target.value)} placeholder="e.g., AI, Security" />
                        </div>
                        <div className="col-md-4 mb-3">
                            <label className="form-label fw-bold">Programming Languages</label>
                            <input type="text" className="form-control" value={languagesInput} onChange={(e) => setLanguagesInput(e.target.value)} placeholder="e.g., Python, C++" />
                        </div>
                        <div className="col-md-4 mb-3">
                            <label className="form-label fw-bold">Project Category</label>
                            <input type="text" className="form-control" value={categoryInput} onChange={(e) => setCategoryInput(e.target.value)} placeholder="e.g., Web App, Research" />
                        </div>
                    </div>
                    <div className="form-text mb-4 mt-neg-2">Separate multiple items in the boxes above using commas.</div>

                    {/* ========================================== */}
                    {/* NEW PRE-AGREEMENT TOGGLE & DROPDOWN */}
                    {/* ========================================== */}
                    <div className="card bg-light border-0 p-4 mb-4 rounded">
                        <div className="form-check form-switch mb-3">
                            <input
                                className="form-check-input"
                                type="checkbox"
                                id="preAgreementToggle"
                                style={{ transform: "scale(1.2)", cursor: "pointer" }}
                                checked={hasPreAgreement}
                                onChange={(e) => {
                                    setHasPreAgreement(e.target.checked);
                                    if (!e.target.checked) setSelectedSupervisor('');
                                }}
                            />
                            <label className="form-check-label fw-bold ms-2 cursor-pointer text-dark" htmlFor="preAgreementToggle">
                                I have already agreed on a project with a specific supervisor.
                            </label>
                        </div>

                        {hasPreAgreement && (
                            <div className="mt-3">
                                <label className="form-label fw-bold text-success">Select your pre-agreed Supervisor:</label>
                                <select
                                    className="form-select border-success"
                                    value={selectedSupervisor}
                                    onChange={(e) => setSelectedSupervisor(e.target.value)}
                                >
                                    <option value="">-- Choose an Academic --</option>
                                    {supervisorList.map((sup) => (
                                        <option key={sup.id} value={sup.name}>
                                            {sup.name}
                                        </option>
                                    ))}
                                </select>
                                <div className="form-text mt-2 text-muted">
                                    <small>By clicking submit, you will bypass the AI algorithm entirely.</small>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* DYNAMIC BUTTON - Changes based on the toggle! */}
                    {hasPreAgreement ? (
                        <button className="btn btn-success w-100 py-3 fw-bold" onClick={handleSubmitPreAgreement} disabled={loading || !name.trim() || !selectedSupervisor}>
                            {loading ? "Saving..." : "✅ Submit Pre-Agreed Proposal"}
                        </button>
                    ) : (
                        <button className="btn btn-primary w-100 py-3 fw-bold" onClick={handleGetSuggestions} disabled={loading || !name.trim()}>
                            {loading ? "✨ AI is analysing..." : "✨ Get AI Supervisor Suggestions"}
                        </button>
                    )}
                </div>
            )}

            {step === 2 && (
                <form onSubmit={handleFinalSubmit}>
                    <div className="alert alert-success">
                        <strong>AI Analysis Complete!</strong> Based on your input, here are the best academic matches for your project:
                    </div>

                    <div className="row mb-4">
                        {suggestions.map((sup) => (
                            <div className="col-md-4 mb-3" key={sup.id}>
                                <div className="card h-100 border-primary">
                                    <div className="card-body text-center">
                                        <h5 className="card-title text-primary">{sup.name}</h5>
                                        <h3 className="text-success">{sup.match_percentage}%</h3>
                                        <p className="card-text small text-muted mb-1">Match Score</p>
                                        <div className="badge bg-secondary text-wrap" style={{ fontSize: "0.7rem" }}>{sup.interests.join(", ")}</div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="card bg-light p-3 mb-4">
                        <label className="form-label fw-bold text-dark">Finalise Your Choices</label>
                        <p className="small text-muted mb-2">Review the AI suggestions above and type your final supervisor preferences below. You may ignore the AI and choose anyone.</p>
                        <input
                            type="text"
                            className="form-control border-primary"
                            placeholder="Dr. Lovelace, Dr. Turing"
                            value={finalPrefs}
                            onChange={(e) => setFinalPrefs(e.target.value)}
                            required
                        />
                        <div className="form-text text-danger mt-2 fw-bold">
                            Maximum allowed: {maxPrefs} supervisors.
                        </div>
                    </div>

                    <div className="d-flex justify-content-between">
                        <button type="button" className="btn btn-outline-secondary" onClick={() => setStep(1)}>
                            ← Edit Proposal
                        </button>
                        <button type="submit" className="btn btn-success fw-bold" disabled={loading}>
                            {loading ? "Saving..." : "Submit Final Proposal"}
                        </button>
                    </div>
                </form>
            )}

            {step === 3 && (
                <div className="text-center py-5">
                    <h2 className="text-success mb-3">✅ Complete!</h2>
                    <p className="lead">{successMessage}</p>
                    <button className="btn btn-outline-primary mt-4 fw-bold" onClick={() => window.location.reload()}>
                        Submit Another Student
                    </button>
                </div>
            )}
        </div>
    );
};

export default StudentProposal;