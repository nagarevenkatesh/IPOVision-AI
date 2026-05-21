import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api/api";
import React from "react";


export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const res = await API.get("/dashboard/");
        setData(res.data);
      } catch (err) {
        localStorage.removeItem("access_token");
        navigate("/login");
      }
    };

    loadDashboard();
  }, [navigate]);

  if (error) {
    return <div style={{ padding: "24px" }}>{error}</div>;
  }

  if (!data) {
    return <div style={{ padding: "24px" }}>Loading dashboard...</div>;
  }

  return (
    <div style={{ padding: "24px", maxWidth: "1100px", margin: "0 auto" }}>
      <h1>Dashboard</h1>
      <p>Track IPOs, predictions, and recent activity.</p>

      <div style={{ display: "flex", gap: "16px", marginTop: "24px", flexWrap: "wrap" }}>
        <div style={{ padding: "16px", border: "1px solid #ddd", borderRadius: "12px", minWidth: "220px", flex: "1" }}>
          <h3>Total IPOs</h3>
          <p style={{ fontSize: "28px", fontWeight: "bold" }}>{data.total_ipos}</p>
        </div>

        <div style={{ padding: "16px", border: "1px solid #ddd", borderRadius: "12px", minWidth: "220px", flex: "1" }}>
          <h3>Total Predictions</h3>
          <p style={{ fontSize: "28px", fontWeight: "bold" }}>{data.total_predictions}</p>
        </div>

        <div style={{ padding: "16px", border: "1px solid #ddd", borderRadius: "12px", minWidth: "220px", flex: "1" }}>
          <h3>Quick Actions</h3>
          <p><Link to="/predict">Create Prediction</Link></p>
          <p><Link to="/history">View History</Link></p>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px", marginTop: "32px" }}>
        <div style={{ padding: "20px", border: "1px solid #ddd", borderRadius: "12px" }}>
          <h2>Latest IPOs</h2>
          {data.latest_ipos?.length ? (
            <ul style={{ paddingLeft: "18px" }}>
              {data.latest_ipos.map((ipo) => (
                <li key={ipo.id} style={{ marginBottom: "10px" }}>
                  <strong>{ipo.company_name}</strong> ({ipo.ticker}) — ₹{ipo.issue_price} — {ipo.sector || "N/A"}
                </li>
              ))}
            </ul>
          ) : (
            <p>No IPOs available.</p>
          )}
        </div>

        <div style={{ padding: "20px", border: "1px solid #ddd", borderRadius: "12px" }}>
          <h2>Recent Predictions</h2>
          {data.recent_predictions?.length ? (
            <ul style={{ paddingLeft: "18px" }}>
              {data.recent_predictions.map((pred) => (
                <li key={pred.id} style={{ marginBottom: "10px" }}>
                  <strong>{pred.company_name}</strong> — {pred.predicted_return}% — {pred.label}
                </li>
              ))}
            </ul>
          ) : (
            <p>No predictions yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}