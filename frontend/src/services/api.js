import axios from 'axios';

// Create an Axios instance with the base URL of our Flask API
const apiClient = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor
// This function runs before every request is sent.
// It checks if a token exists in localStorage and adds it to the Authorization header.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
