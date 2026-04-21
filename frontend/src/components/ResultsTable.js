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
                    <ul className="mb-0 list-unstyled">
                {unallocated.map((student, idx) => (
                    <li key={idx} className="mb-3 p-3 bg-white rounded border border-danger shadow-sm">
                        <span className="fw-bold text-danger fs-5">{student.name}</span>
                        
                        <div className="text-dark mt-2 mb-2" style={{ fontSize: "0.95rem" }}>
                            <strong>Topic:</strong> <span className={student.topic === "No specific topic provided." ? "text-muted font-italic" : ""}>{student.topic}</span>
                        </div>
                        
                        {/* Render Skills Badges if they exist */}
                        {student.skills && student.skills.length > 0 && (
                            <div className="mb-1">
                                <strong className="small text-muted text-uppercase me-2">Skills:</strong>
                                {student.skills.map((skill, s_idx) => (
                                    <span key={s_idx} className="badge bg-secondary me-1">{skill}</span>
                                ))}
                            </div>
                        )}

                        {/* Render Format Badges if they exist */}
                        {student.format && student.format.length > 0 && (
                            <div>
                                <strong className="small text-muted text-uppercase me-2">Format:</strong>
                                {student.format.map((fmt, f_idx) => (
                                    <span key={f_idx} className="badge bg-light text-dark border border-secondary me-1">{fmt}</span>
                                ))}
                            </div>
                        )}
                    </li>
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