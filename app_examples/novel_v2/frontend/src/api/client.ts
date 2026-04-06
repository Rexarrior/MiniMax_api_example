import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

client.interceptors.request.use(
  (config) => {
    const sessionId = localStorage.getItem('session_id')
    if (sessionId) {
      config.headers['X-Session-ID'] = sessionId
    }
    return config
  },
  (error) => Promise.reject(error)
)

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 404) {
      console.error('Resource not found:', error.config.url)
    }
    return Promise.reject(error)
  }
)

export default client
