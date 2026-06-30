import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8001";
const API_TOKEN = import.meta.env.VITE_API_SECRET_TOKEN || "";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    Authorization: `Bearer ${API_TOKEN}`,
  },
});

export default api;
