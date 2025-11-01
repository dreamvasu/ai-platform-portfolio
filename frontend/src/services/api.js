import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getTechStack = async () => {
  const response = await api.get('/tech-stack/');
  return response.data;
};

export const getTechStackByCategory = async () => {
  const response = await api.get('/tech-stack/by_category/');
  return response.data;
};

export const getJourneyEntries = async () => {
  const response = await api.get('/journey/');
  return response.data;
};

export const getProjects = async () => {
  const response = await api.get('/projects/');
  return response.data;
};

export const getFeaturedProjects = async () => {
  const response = await api.get('/projects/featured/');
  return response.data;
};

export default api;
