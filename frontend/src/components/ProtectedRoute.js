import React from 'react';
import { Navigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

const ProtectedRoute = ({ children, allowedRoles }) => {
    const token = localStorage.getItem('access_token');

    if (!token) {
        return <Navigate to="/login" replace />;
    }

    try {
        const decodedToken = jwtDecode(token);
        const userRole = decodedToken.role;

        if (allowedRoles.includes(userRole)) {
            return children;
        } else {
            console.warn(`Unauthorised access attempt by role: ${userRole}`);
            return <Navigate to="/unauthorised" replace />;
        }
    } catch (error) {
        console.error("Invalid token:", error);
        return <Navigate to="/login" replace />;
    }
};

export default ProtectedRoute;