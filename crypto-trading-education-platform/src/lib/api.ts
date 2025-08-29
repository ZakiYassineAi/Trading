import axios from 'axios';
import { getTokens, setTokens, clearTokens } from './utils';

export const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:3000',
});

api.interceptors.response.use(
  res => res,
  async error => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const tokens = getTokens();
      if (tokens?.refreshtoken) {
        try {
          const { data } = await axios.post('/auth/refresh', { refreshtoken: tokens.refreshtoken });
          setTokens(data);
          originalRequest.headers['Authorization'] = `Bearer ${data.accesstoken}`;
          return api(originalRequest);
        } catch {
          clearTokens();
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);
