import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
});

let token = null;

const setToken = (newToken) => {
  token = newToken;
  if (newToken) {
    api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Manejar error de autenticación (por ejemplo, redirigir a login)
    }
    return Promise.reject(error);
  }
);

export default {
  setToken,
  get: api.get,
  post: api.post,
  put: api.put,
  delete: api.delete,
};
