import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select';
import CreatableSelect from 'react-select/creatable';

const StudentProposal = () => {

    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');
    const [showCategoryHelp, setShowCategoryHelp] = useState(false);

    const [maxPrefs, setMaxPrefs] = useState(3);
    const [name, setName] = useState("");
    const [topic, setTopic] = useState("");

    const [selectedInterests, setSelectedInterests] = useState([]);
    const [selectedSkills, setSelectedSkills] = useState([]);
    const [selectedCategories, setSelectedCategories] = useState([]);

    const [finalPrefs, setFinalPrefs] = useState("");
    const [hasPreAgreement, setHasPreAgreement] = useState(false);
    const [selectedSupervisor, setSelectedSupervisor] = useState("");
    const [supervisorList, setSupervisorList] = useState([]);
    const [suggestions, setSuggestions] = useState([]);

    const [categoryOptions, setCategoryOptions] = useState([]);
    const [skillOptions, setSkillOptions] = useState([]);
    const [interestOptions, setInterestOptions] = useState([]);

    const wordCount = topic.trim() === '' ? 0 : topic.trim().split(/\s+/).length;

    useEffect(() => {
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

        fetchConfig();
        fetchSupervisors();
        fetchTaxonomies();
    }, []);

    const handleCategoryChange = (selectedOptions) => {
        if (selectedOptions && selectedOptions.length > 2) {
            alert("You may only select a maximum of two project categories.");
        } else {
            setSelectedCategories(selectedOptions || []);
        }
    };

    const handleGetSuggestions = async () => {
        setError(null);
        if (wordCount > 200) return setError(`Topic is too long. Limit: 200 words (currently ${wordCount}).`);
        if (!topic.trim() && selectedInterests.length === 0 && selectedSkills.length === 0 && selectedCategories.length === 0) {
            return setError("Please provide a topic description or select some skills/categories.");
        }

        setLoading(true);
        try {
            const combinedKeywords = [
                ...selectedInterests.map(i => i.value),
                ...selectedSkills.map(s => s.value),
                ...selectedCategories.map(f => f.value)
            ];

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
                interests: selectedInterests.map(i => i.value),
                technical_skills: selectedSkills.map(s => s.value),
                project_category: selectedCategories.map(f => f.value), // FIXED
                preferences: [], 
                has_pre_agreement: true,
                pre_agreed_supervisor: selectedSupervisor
            };

            await axios.post('http://127.0.0.1:8000/allocation/add-student/', payload);
            setSuccessMessage(`Success! Your pre-agreement with ${selectedSupervisor} has been officially recorded. You will bypass the matching algorithm.`);
            setStep(3); 
        } catch (err) {
            setError(err.response?.data?.message || 'Error: Could not add student.');
        } finally {
            setLoading(false);
        }
    };

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
                interests: selectedInterests.map(i => i.value),
                technical_skills: selectedSkills.map(s => s.value),
                project_category: selectedCategories.map(f => f.value), // FIXED
                preferences: preferencesArray,
                has_pre_agreement: false,
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
                        <div className="col-md-12 mb-3">
                            <label className="form-label fw-bold">Research Interests</label>
                            <CreatableSelect
                                isMulti
                                options={interestOptions}
                                value={selectedInterests}
                                onChange={(opts) => setSelectedInterests(opts || [])}
                                placeholder="Type an interest and press Enter..."
                                formatCreateLabel={(inputValue) => `Add "${inputValue}"`}
                            />
                        </div>
                        <div className="col-md-12 mb-3">
                            <label className="form-label fw-bold">Technical Skills</label>
                            <CreatableSelect
                                isMulti
                                options={skillOptions}
                                value={selectedSkills}
                                onChange={(opts) => setSelectedSkills(opts || [])}
                                placeholder="Type a skill/language and press Enter..."
                                formatCreateLabel={(inputValue) => `Add "${inputValue}"`}
                            />
                        </div>
                        <div className="col-md-12 mb-4">
                            <label className="form-label fw-bold d-flex align-items-center mb-2">
                                Project Category
                                <span 
                                className="badge bg-light text-secondary border border-primary ms-2 rounded-1"
                                onClick={() => setShowCategoryHelp(!showCategoryHelp)}
                                style={{ cursor: "pointer", fontSize: "0.8rem", padding: "0.4em 0.6em" }}
                                >
                                    ?
                                </span>
                            </label>
                            {showCategoryHelp && (
                                <div className="alert alert-secondary py-2 px-3 mb-3 shadow-sm" style={{ fontSize: "0.85rem" }}>
                                    <strong>What is a Project Category?</strong> It defines the primary output of your project. For example, are you building a software system, conducting theoretical research, or analysing data? <em>(Maximum 2 allowed)</em>
                                </div>
                            )}
                            <Select
                                isMulti
                                options={categoryOptions} 
                                value={selectedCategories}
                                onChange={handleCategoryChange}
                                placeholder="Select up to 2 categories..."
                            />
                        </div>
                    </div>

                    <div className="card bg-light border-0 p-4 mb-4 rounded">
                        <div className="form-check form-switch mb-3">
                            <input className="form-check-input" type="checkbox" id="preAgreementToggle" style={{ transform: "scale(1.2)", cursor: "pointer" }} checked={hasPreAgreement} onChange={(e) => { setHasPreAgreement(e.target.checked); if (!e.target.checked) setSelectedSupervisor(''); }} />
                            <label className="form-check-label fw-bold ms-2 cursor-pointer text-dark" htmlFor="preAgreementToggle">
                                I have already agreed on a project with a specific supervisor.
                            </label>
                        </div>
                        {hasPreAgreement && (
                            <div className="mt-3">
                                <label className="form-label fw-bold text-success">Select your pre-agreed Supervisor:</label>
                                <select className="form-select border-success" value={selectedSupervisor} onChange={(e) => setSelectedSupervisor(e.target.value)}>
                                    <option value="">-- Choose an Academic --</option>
                                    {supervisorList.map((sup) => (
                                        <option key={sup.id} value={sup.name}>{sup.name}</option>
                                    ))}
                                </select>
                            </div>
                        )}
                    </div>

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
                    <div className="alert alert-success"><strong>AI Analysis Complete!</strong></div>
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
                        <input type="text" className="form-control border-primary" placeholder="Dr. Lovelace, Dr. Turing" value={finalPrefs} onChange={(e) => setFinalPrefs(e.target.value)} required />
                    </div>

                    <div className="d-flex justify-content-between">
                        <button type="button" className="btn btn-outline-secondary" onClick={() => setStep(1)}>← Edit Proposal</button>
                        <button type="submit" className="btn btn-success fw-bold" disabled={loading}>Submit Final Proposal</button>
                    </div>
                </form>
            )}

            {step === 3 && (
                <div className="text-center py-5">
                    <h2 className="text-success mb-3">✅ Complete!</h2>
                    <p className="lead">{successMessage}</p>
                    <button className="btn btn-outline-primary mt-4 fw-bold" onClick={() => window.location.reload()}>Submit Another Student</button>
                </div>
            )}
        </div>
    );
};

export default StudentProposal;