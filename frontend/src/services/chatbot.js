import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';
const CHATBOT_BASE_URL = `${API_BASE}/chatbot`;

const chatbotApi = axios.create({
  baseURL: CHATBOT_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const sendChatMessage = async (question, k = 5, include_sources = true) => {
  const response = await chatbotApi.post('/query/', {
    question,
    k,
    include_sources,
  });
  return response.data;
};

export const getSuggestedQuestions = async () => {
  const response = await chatbotApi.get('/suggestions/');
  return response.data;
};

export const getChatbotHealth = async () => {
  const response = await chatbotApi.get('/health/');
  return response.data;
};

export default chatbotApi;
