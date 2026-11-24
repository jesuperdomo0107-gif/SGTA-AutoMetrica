// src/services/api.js
// Instancia base de Axios apuntando al backend de FastAPI (local o Render)
import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL.replace(/\/$/, "")}/api/v1`
  : "/api/v1";

const api = axios.create({
  baseURL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor global de peticiones: inyecta el token JWT Bearer automáticamente
api.interceptors.request.use((config) => {
  try {
    const raw = localStorage.getItem("autometrica_usuario");
    if (raw) {
      const user = JSON.parse(raw);
      if (user?.access_token) {
        config.headers.Authorization = `Bearer ${user.access_token}`;
      }
    }
  } catch (err) {
    console.warn("No se pudo leer el token de autenticación:", err);
  }
  return config;
});

// Interceptor global de errores: muestra el mensaje del backend si existe
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const msg =
      error.response?.data?.detail ||
      "Error de conexión con el servidor backend (FastAPI). Si estás en Render (plan gratuito), espera ~30 segundos mientras despierta el servidor.";
    return Promise.reject(new Error(msg));
  }
);

export default api;
