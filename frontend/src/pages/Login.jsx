import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api/api";
import React from "react";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await API.post("/auth/login", { username, password });
      localStorage.setItem("access_token", res.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError(err?.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div style={{ padding: "24px", maxWidth: "420px", margin: "0 auto" }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "12px" }}>
          <label>Username</label>
          <input
            style={{ width: "100%", padding: "10px", marginTop: "6px" }}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div style={{ marginBottom: "12px" }}>
          <label>Password</label>
          <input
            type="password"
            style={{ width: "100%", padding: "10px", marginTop: "6px" }}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        {error && <p style={{ color: "red" }}>{error}</p>}

        <button type="submit" style={{ padding: "10px 16px" }}>
          Login
        </button>
      </form>

      <p style={{ marginTop: "12px" }}>
        No account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
}