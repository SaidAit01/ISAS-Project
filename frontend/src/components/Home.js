import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
    return (
        <div className="jumbotron p-5 bg-light rounded text-center">
            <h1 className="display-4">Intelligent Student Allocation System</h1>
            <p className="lead">
                A Hybrid AI approach to solving the Student-Project Allocation problem.
            </p>
            <hr className="my-4" />
            <p>
                This system utilizes <strong>SBERT (Semantic Search)</strong> combined with the
                <strong> SPA Algorithm</strong> to ensure fair and optimal matches.
            </p>
            <Link className="btn btn-primary btn-lg" to="/allocation" role="button">
                Start Allocation
            </Link>
        </div>
    );
};

export default Home;