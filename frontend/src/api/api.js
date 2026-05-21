import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api/v1",
});

API.interceptors.request.use((cfg) => {
  const token = localStorage.getItem("access_token");
  if (token) cfg.headers.Authorization = `Bearer ${token}`;
  return cfg;
});

export default API;