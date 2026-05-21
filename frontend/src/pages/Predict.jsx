import React, { useEffect, useState } from "react";
import API from "../api/api";

export default function Predict() {
  const [ipos, setIpos] = useState([]);
  const [ipoId, setIpoId] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadIpos = async () => {
      try {
        const res = await API.get("/ipos/");
        setIpos(Array.isArray(res.data) ? res.data : []);
      } catch (err) {
        console.error(err);
        setError("Failed to load IPO list");
      }
    };

    loadIpos();
  }, []);

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await API.post("/predictions/", {
        ipo_id: Number(ipoId),
      });
      setResult(res.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "24px", maxWidth: "800px", margin: "0 auto" }}>
      <h1>Predict IPO Return</h1>
      <p>Select an IPO and generate a prediction.</p>

      <form
        onSubmit={handlePredict}
        style={{
          marginTop: "24px",
          padding: "20px",
          border: "1px solid #ddd",
          borderRadius: "12px",
        }}
      >
        <div style={{ marginBottom: "16px" }}>
          <label>Select IPO</label>
          <select
            style={{ width: "100%", padding: "10px", marginTop: "6px" }}
            value={ipoId}
            onChange={(e) => setIpoId(e.target.value)}
          >
            <option value="">Choose IPO</option>
            {ipos.length > 0 ? (
              ipos.map((ipo) => (
                <option key={ipo.id} value={ipo.id}>
                  {ipo.company_name} ({ipo.ticker})
                </option>
              ))
            ) : (
              <option value="" disabled>
                No IPOs available
              </option>
            )}
          </select>
        </div>

        {error && <p style={{ color: "red" }}>{error}</p>}

        <button
          type="submit"
          disabled={loading || !ipoId}
          style={{ padding: "10px 16px" }}
        >
          {loading ? "Predicting..." : "Predict"}
        </button>
      </form>

      {result && (
        <div
          style={{
            marginTop: "24px",
            padding: "20px",
            border: "1px solid #ddd",
            borderRadius: "12px",
          }}
        >
          <h2>Prediction Result</h2>
          <p><strong>IPO ID:</strong> {result.ipo_id}</p>
          <p><strong>Predicted Return:</strong> {result.predicted_return}%</p>
          <p><strong>Confidence Score:</strong> {result.confidence_score ?? "N/A"}</p>
          <p><strong>Model Version:</strong> {result.model_version}</p>
        </div>
      )}
    </div>
  );
}