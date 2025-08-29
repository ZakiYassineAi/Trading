import axios from 'axios'

// Create axios instance with default config
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3001/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle common errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  login: (email: string, password: string) =>
    apiClient.post('/auth/login', { email, password }),
  register: (email: string, password: string, fullName: string) =>
    apiClient.post('/auth/register', { email, password, fullName }),
  logout: () => apiClient.post('/auth/logout'),
  me: () => apiClient.get('/auth/me')
}

// Trading API
export const tradingApi = {
  getPortfolio: () => apiClient.get('/portfolio'),
  getStrategies: () => apiClient.get('/strategies'),
  createStrategy: (strategy: any) => apiClient.post('/strategies', strategy),
  updateStrategy: (id: string, strategy: any) => apiClient.put(`/strategies/${id}`, strategy),
  deleteStrategy: (id: string) => apiClient.delete(`/strategies/${id}`),
  backtestStrategy: (params: any) => apiClient.post('/backtest', params),
  getMarketData: (symbol: string) => apiClient.get(`/market/${symbol}`)
}

// DeFi API
export const defiApi = {
  getProtocols: () => apiClient.get('/defi/protocols'),
  getPositions: () => apiClient.get('/defi/positions'),
  stake: (protocol: string, amount: number) => apiClient.post('/defi/stake', { protocol, amount }),
  unstake: (positionId: string) => apiClient.post(`/defi/unstake/${positionId}`)
}