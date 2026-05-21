import { Link, useNavigate } from "react-router-dom";
import React from "react";

export default function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  return (
    <nav
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "16px 24px",
        background: "#111827",
        color: "white",
      }}
    >
      <Link to="/" style={{ color: "white", fontWeight: "bold" }}>
        IPO Insight Platform
      </Link>

      <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
        <Link to="/dashboard" style={{ color: "white" }}>Dashboard</Link>
        <Link to="/predict" style={{ color: "white" }}>Predict</Link>
        <Link to="/history" style={{ color: "white" }}>History</Link>
        {!token ? (
          <>
            <Link to="/login" style={{ color: "white" }}>Login</Link>
            <Link to="/register" style={{ color: "white" }}>Register</Link>
          </>
        ) : (
          <button onClick={handleLogout} style={{ padding: "8px 12px" }}>
            Logout
          </button>
        )}
      </div>
    </nav>
  );
}