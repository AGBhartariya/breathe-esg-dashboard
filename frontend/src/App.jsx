import "./App.css";

import axios from "axios";

import { useEffect, useState } from "react";

function App() {

    const [activities, setActivities] = useState([]);

    const [issues, setIssues] = useState([]);

    const [batches, setBatches] = useState([]);

    const [file, setFile] = useState(null);

    const [sourceType, setSourceType] = useState("SAP");

    const [statusFilter, setStatusFilter] = useState("all");

    const [showSuspiciousOnly, setShowSuspiciousOnly] =
        useState(false);

    // =========================================
    // FETCH ACTIVITIES
    // =========================================

    const fetchActivities = async () => {

        try {

            const response = await axios.get(
                "http://127.0.0.1:8000/api/activities/"
            );

            setActivities(response.data);

        } catch (error) {

            console.error(error);
        }
    };

    // =========================================
    // FETCH ISSUES
    // =========================================

    const fetchIssues = async () => {

        try {

            const response = await axios.get(
                "http://127.0.0.1:8000/api/issues/"
            );

            setIssues(response.data);

        } catch (error) {

            console.error(error);
        }
    };

    // =========================================
    // FETCH BATCHES
    // =========================================

    const fetchBatches = async () => {

        try {

            const response = await axios.get(
                "http://127.0.0.1:8000/api/batches/"
            );

            setBatches(response.data);

        } catch (error) {

            console.error(error);
        }
    };

    // =========================================
    // INITIAL LOAD
    // =========================================

    useEffect(() => {

        fetchActivities();

        fetchIssues();

        fetchBatches();

    }, []);

    // =========================================
    // HANDLE FILE UPLOAD
    // =========================================

    const handleUpload = async () => {

        if (!file) {

            alert("Please select a file");

            return;
        }

        const formData = new FormData();

        formData.append("file", file);

        formData.append(
            "source_type",
            sourceType
        );

        try {

            await axios.post(
                "http://127.0.0.1:8000/api/upload/",
                formData
            );

            fetchActivities();

            fetchIssues();

            fetchBatches();

            alert("Upload successful");

        } catch (error) {

            console.error(error);

            alert("Upload failed");
        }
    };

    // =========================================
    // APPROVE
    // =========================================

    const approveActivity = async (id) => {

        try {

            await axios.post(
                `http://127.0.0.1:8000/api/approve/${id}/`
            );

            fetchActivities();

        } catch (error) {

            console.error(error);
        }
    };

    // =========================================
    // REJECT
    // =========================================

    const rejectActivity = async (id) => {

        try {

            await axios.post(
                `http://127.0.0.1:8000/api/reject/${id}/`
            );

            fetchActivities();

        } catch (error) {

            console.error(error);
        }
    };

    // =========================================
    // FILTERS
    // =========================================

    const filteredActivities = activities.filter(
        (activity) => {

            const matchesStatus =

                statusFilter === "all"

                ||

                activity.review_status === statusFilter;

            const matchesSuspicious =

                !showSuspiciousOnly

                ||

                activity.is_suspicious;

            return (
                matchesStatus
                &&
                matchesSuspicious
            );
        }
    );

    // =========================================
    // STATS
    // =========================================

    const totalRecords = activities.length;

    const approvedCount = activities.filter(
        (a) => a.review_status === "approved"
    ).length;

    const rejectedCount = activities.filter(
        (a) => a.review_status === "rejected"
    ).length;

    const pendingCount = activities.filter(
        (a) => a.review_status === "pending"
    ).length;

    const suspiciousCount = activities.filter(
        (a) => a.is_suspicious
    ).length;

    return (

        <div className="app-container">

            {/* ========================================= */}
            {/* TITLE */}
            {/* ========================================= */}

            <h1 className="main-title">
                Breathe ESG Dashboard
            </h1>

            {/* ========================================= */}
            {/* STATS */}
            {/* ========================================= */}

            <div className="stats-grid">

                <div className="stat-card">

                    <h3>Total Records</h3>

                    <p>{totalRecords}</p>

                </div>

                <div className="stat-card pending">

                    <h3>Pending</h3>

                    <p>{pendingCount}</p>

                </div>

                <div className="stat-card approved">

                    <h3>Approved</h3>

                    <p>{approvedCount}</p>

                </div>

                <div className="stat-card rejected">

                    <h3>Rejected</h3>

                    <p>{rejectedCount}</p>

                </div>

                <div className="stat-card suspicious">

                    <h3>Suspicious</h3>

                    <p>{suspiciousCount}</p>

                </div>

            </div>

            {/* ========================================= */}
            {/* UPLOAD */}
            {/* ========================================= */}

            <div className="upload-card">

                <h2>Upload ESG Data</h2>

                <div className="upload-controls">

                    <select
                        value={sourceType}
                        onChange={(e) =>
                            setSourceType(
                                e.target.value
                            )
                        }
                    >

                        <option>SAP</option>

                        <option>Utility</option>

                        <option>Travel</option>

                    </select>

                    <input
                        type="file"
                        onChange={(e) =>
                            setFile(
                                e.target.files[0]
                            )
                        }
                    />

                    <button
                        onClick={handleUpload}
                    >

                        Upload

                    </button>

                </div>

            </div>

            {/* ========================================= */}
            {/* FILTERS */}
            {/* ========================================= */}

            <div className="filter-section">

                <div>

                    <label>
                        Filter Status:
                    </label>

                    {" "}

                    <select
                        value={statusFilter}
                        onChange={(e) =>
                            setStatusFilter(
                                e.target.value
                            )
                        }
                    >

                        <option value="all">
                            All
                        </option>

                        <option value="pending">
                            Pending
                        </option>

                        <option value="approved">
                            Approved
                        </option>

                        <option value="rejected">
                            Rejected
                        </option>

                    </select>

                </div>

                <div className="checkbox-group">

                    <input
                        type="checkbox"
                        checked={
                            showSuspiciousOnly
                        }
                        onChange={() =>
                            setShowSuspiciousOnly(
                                !showSuspiciousOnly
                            )
                        }
                    />

                    <label>
                        Suspicious Only
                    </label>

                </div>

            </div>

            {/* ========================================= */}
            {/* ACTIVITIES TABLE */}
            {/* ========================================= */}

            <table>

                <thead>

                    <tr>

                        <th>Activity ID</th>

                        <th>Activity</th>

                        <th>Vendor</th>

                        <th>Raw Quantity</th>

                        <th>Normalized Quantity</th>

                        <th>Status</th>

                        <th>Source</th>

                        <th>Company</th>

                        <th>Upload Batch</th>

                        <th>Suspicious</th>

                        <th>Actions</th>

                    </tr>

                </thead>

                <tbody>

                    {filteredActivities.map(
                        (activity) => (

                            <tr
                                key={activity.id}
                            >

                                <td>
                                    {activity.id}
                                </td>

                                <td>
                                    {
                                        activity.activity_type
                                    }
                                </td>

                                <td>
                                    {activity.vendor}
                                </td>

                                <td>

                                    {
                                        activity.quantity
                                    }

                                    {" "}

                                    {activity.unit}

                                </td>

                                <td>

                                    {
                                        activity.normalized_quantity
                                    }

                                    {" "}

                                    {
                                        activity.normalized_unit
                                    }

                                </td>

                                <td>

                                    <span
                                        className={`status-badge ${activity.review_status}`}
                                    >

                                        {
                                            activity.review_status
                                        }

                                    </span>

                                </td>

                                <td>
                                    {
                                        activity.source_type
                                    }
                                </td>

                                <td>
                                    {
                                        activity.company_name
                                    }
                                </td>

                                <td>
                                    {
                                        activity.batch_id
                                    }
                                </td>

                                <td>

                                    {
                                        activity.is_suspicious

                                        ?

                                        <span className="suspicious-pill">

                                            ⚠ {

                                                activity.suspicious_reason

                                                ?

                                                activity.suspicious_reason
                                                    .split(";")
                                                    .length

                                                :

                                                1
                                            }

                                            {" "}

                                            Issues

                                        </span>

                                        :

                                        <span className="clean-tag">

                                            Clean

                                        </span>
                                    }

                                </td>

                                <td>

                                    <div className="action-buttons">

                                        <button
                                            className="approve-btn"
                                            onClick={() =>
                                                approveActivity(
                                                    activity.id
                                                )
                                            }
                                        >

                                            Approve

                                        </button>

                                        <button
                                            className="reject-btn"
                                            onClick={() =>
                                                rejectActivity(
                                                    activity.id
                                                )
                                            }
                                        >

                                            Reject

                                        </button>

                                    </div>

                                </td>

                            </tr>
                        )
                    )}

                </tbody>

            </table>

            {/* ========================================= */}
            {/* BATCHES */}
            {/* ========================================= */}

            <div className="batch-section">

                <h2>
                    Recent Upload Batches
                </h2>

                <table>

                    <thead>

                        <tr>

                            <th>Batch ID</th>

                            <th>Source</th>

                            <th>Company</th>

                            <th>Total Rows</th>

                            <th>Success</th>

                            <th>Failed</th>

                            <th>Suspicious</th>

                            <th>Status</th>

                            <th>Uploaded At</th>

                        </tr>

                    </thead>

                    <tbody>

                        {batches.map((batch) => (

                            <tr key={batch.id}>

                                <td>{batch.id}</td>

                                <td>
                                    {batch.source_type}
                                </td>

                                <td>
                                    {batch.company_name}
                                </td>

                                <td>
                                    {batch.total_rows}
                                </td>

                                <td>
                                    {batch.success_rows}
                                </td>

                                <td>
                                    {batch.failed_rows}
                                </td>

                                <td>
                                    {
                                        batch.suspicious_rows
                                    }
                                </td>

                                <td>

                                    {
                                        batch.status
                                            .replaceAll(
                                                "_",
                                                " "
                                            )
                                    }

                                </td>

                                <td>

                                    {

                                        new Date(
                                            batch.uploaded_at
                                        ).toLocaleString()

                                    }

                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

            {/* ========================================= */}
            {/* ISSUES */}
            {/* ========================================= */}

            <div className="issues-section">

                <h2>
                    Detected Data Issues
                </h2>

                <table>

                    <thead>

                        <tr>

                            <th>Issue Ref</th>

                            <th>Activity Ref</th>

                            <th>Type</th>

                            <th>Severity</th>

                            <th>Message</th>

                        </tr>

                    </thead>

                    <tbody>

                        {issues.map((issue) => (

                            <tr key={issue.id}>

                                <td>
                                    {issue.id}
                                </td>

                                <td>
                                    {
                                        issue.activity
                                    }
                                </td>

                                <td>
                                    {
                                        issue.issue_type
                                    }
                                </td>

                                <td>
                                    {
                                        issue.severity
                                    }
                                </td>

                                <td>
                                    {
                                        issue.issue_message
                                    }
                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </div>
    );
}

export default App;