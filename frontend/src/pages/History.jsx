import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/api";
import React from "react";

export default function History() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const res = await API.get("/predictions/");
        setHistory(res.data);
      } catch (err) {
        localStorage.removeItem("access_token");
        navigate("/login");
      }
    };

    loadHistory();
  }, [navigate]);

  if (error) {
    return <div style={{ padding: "24px" }}>{error}</div>;
  }

  return (
    <div style={{ padding: "24px", maxWidth: "1000px", margin: "0 auto" }}>
      <h1>Prediction History</h1>
      <p>All your past IPO predictions in one place.</p>

      <div style={{ marginTop: "24px" }}>
        {history.length ? (
          history.map((item) => (
            <div
              key={item.id}
              style={{
                marginBottom: "16px",
                padding: "16px",
                border: "1px solid #ddd",
                borderRadius: "12px",
              }}
            >
              <p><strong>IPO ID:</strong> {item.ipo_id}</p>
              <p><strong>Predicted Return:</strong> {item.predicted_return}%</p>
              <p><strong>Confidence Score:</strong> {item.confidence_score ?? "N/A"}</p>
              <p><strong>Model Version:</strong> {item.model_version}</p>
              <p><strong>Created At:</strong> {item.created_at}</p>
            </div>
          ))
        ) : (
          <p>No prediction history yet.</p>
        )}
      </div>
    </div>
  );
}