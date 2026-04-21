import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            // Hit the Django JWT login endpoint
            const response = await axios.post('http://127.0.0.1:8000/allocation/api/login/', {
                username,
                password
            });

            // Extract the token and save it to the browser
            const token = response.data.access;
            localStorage.setItem('access_token', token);

            // Decode the token to find out who just logged in
            const decodedToken = jwtDecode(token);
            const role = decodedToken.role;

            // Route them to their specific dashboard
            if (role === 'Project_Coordinator') {
                navigate('/allocation');
            } else if (role === 'Supervisor') {
                navigate('/supervisor');
            } else if (role === 'Student') {
                navigate('/add-student');
            } else {
                navigate('/');
            }

        } catch (err) {
            // Print the full error to the browser console
            console.error("FULL LOGIN ERROR:", err);
            
            // Try to show the exact message from Django, otherwise show the network error
            const exactError = err.response?.data?.detail || err.message || "Failed to connect to server.";
            setError(`Error: ${exactError}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-5 pt-5 max-w-md mx-auto">
            <div className="card shadow-sm border-0 border-top border-primary border-4 p-5">
                <h2 className="fw-bold text-center mb-4">🔐 System Login</h2>
                
                {error && <div className="alert alert-danger fw-bold">{error}</div>}

                <form onSubmit={handleLogin}>
                    <div className="mb-3">
                        <label className="form-label fw-bold">Username</label>
                        <input 
                            type="text" 
                            className="form-control form-control-lg" 
                            value={username} 
                            onChange={(e) => setUsername(e.target.value)} 
                            required 
                        />
                    </div>
                    
                    <div className="mb-4">
                        <label className="form-label fw-bold">Password</label>
                        <input 
                            type="password" 
                            className="form-control form-control-lg" 
                            value={password} 
                            onChange={(e) => setPassword(e.target.value)} 
                            required 
                        />
                    </div>

                    <button 
                        type="submit" 
                        className="btn btn-primary btn-lg w-100 fw-bold" 
                        disabled={loading}
                    >
                        {loading ? "Authenticating..." : "Log In"}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;