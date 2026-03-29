import React from 'react';

// Accept matched, unallocated, and pending data from the parent
const ResultsTable = ({ matched, unallocated, pending }) => {
    if (!matched) return null;

    // Convert the matched dictionary for the table
    const rows = Object.entries(matched);

    return (
        <div className="mt-4">
            <h4 className="mb-3">Allocation Results</h4>

            {/* 1. THE MAIN TABLE */}
            <div className="table-responsive">
                <table className="table table-striped table-bordered">
                    <thead className="table-dark">
                        <tr>
                            <th>Supervisor</th>
                            <th>Assigned Students</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows.map(([supervisor, students], index) => (
                            <tr key={index}>
                                <td className="fw-bold">{supervisor}</td>
                                <td>
                                    {students.length > 0 ? (
                                        students.map((studentName, idx) => (
                                            <span key={idx} className="badge bg-primary me-1">
                                                {studentName}
                                            </span>
                                        ))
                                    ) : (
                                        <span className="text-muted">No Match</span>
                                    )}
                                </td>
                                <td>
                                    {students.length > 0 ? (
                                        <span className="text-success fw-bold">Filled</span>
                                    ) : (
                                        <span className="text-warning fw-bold">Empty</span>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* 2. UNALLOCATED STUDENTS (Red Box) */}
            {unallocated && unallocated.length > 0 && (
                <div className="mt-4 alert alert-danger shadow-sm">
                    <h5 className="alert-heading border-bottom border-danger pb-2">
                        ⚠️ Unallocated Students
                    </h5>
                    <p className="mb-2 mt-2">
                        The following students could not be matched due to capacity limits. Manual intervention required:
                    </p>
                    <ul className="mb-0">
                        {unallocated.map((studentName, idx) => (
                            <li key={idx} className="fw-bold">{studentName}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* 3. PENDING/GHOST STUDENTS (Grey Box) */}
            {pending && pending.length > 0 && (
                <div className="mt-4 alert alert-secondary shadow-sm">
                    <h5 className="alert-heading border-bottom border-secondary pb-2">
                        👻 Pending Submissions (No Data)
                    </h5>
                    <p className="mb-2 mt-2">
                        The following students have not submitted their preferences. They were excluded from the allocation algorithm:
                    </p>
                    <ul className="mb-0">
                        {pending.map((studentName, idx) => (
                            <li key={idx} className="fw-bold text-muted">{studentName}</li>
                        ))}
                    </ul>
                </div>
            )}

        </div>
    );
};

export default ResultsTable;