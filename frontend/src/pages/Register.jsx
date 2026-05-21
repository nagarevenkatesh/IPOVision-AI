import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api/api";
import React from "react";

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await API.post("/auth/register", {
        username,
        email: email || null,
        password,
      });
      navigate("/login");
    } catch (err) {
  console.error(err);
  setError(err?.response?.data?.detail || JSON.stringify(err?.response?.data) || "Registration failed");
    }
  };

  return (
    <div style={{ padding: "24px", maxWidth: "420px", margin: "0 auto" }}>
      <h2>Register</h2>
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
          <label>Email</label>
          <input
            type="email"
            style={{ width: "100%", padding: "10px", marginTop: "6px" }}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
          Register
        </button>
      </form>

      <p style={{ marginTop: "12px" }}>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  );
}