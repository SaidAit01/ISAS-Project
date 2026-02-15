import React from 'react';

const ResultsTable = ({ matches }) => {
    if (!matches) return null;

    // Convert data for the table
    const rows = Object.entries(matches);

    return (
        <div className="mt-4">
            <h4 className="mb-3">Allocation Results</h4>
            <div className="table-responsive">
                <table className="table table-striped table-bordered">
                    <thead className="table-dark">
                        <tr>
                            <th>Supervisor</th>
                            <th>Student ID</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows.map(([supervisor, students], index) => (
                            <tr key={index}>
                                <td className="fw-bold">{supervisor}</td>
                                <td>
                                    {students.length > 0 ? (
                                        students.map(id => (
                                            <span key={id} className="badge bg-primary me-1">
                                                Student #{id}
                                            </span>
                                        ))
                                    ) : (
                                        <span className="text-muted">No Match</span>
                                    )}
                                </td>
                                <td>
                                    {students.length > 0 ? (
                                        <span className="text-success">Filled</span>
                                    ) : (
                                        <span className="text-warning">Empty</span>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ResultsTable;