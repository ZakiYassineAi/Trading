import './App.css'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'react-hot-toast'
import { Navbar } from './components/layout/Navbar'
import { Sidebar } from './components/layout/Sidebar'
import { AuthProvider } from './contexts/AuthContext'
import { ThemeProvider } from './contexts/ThemeContext'
import { Dashboard } from './pages/Dashboard'
import { Strategies } from './pages/Strategies'
import { Backtest } from './pages/Backtest'
import { Portfolio } from './pages/Portfolio'
import { Analytics } from './pages/Analytics'
import { DeFi } from './pages/DeFi'
import { Login } from './pages/Login'
import { Register } from './pages/Register'
import { Settings } from './pages/Settings'
import { ProtectedRoute } from './components/auth/ProtectedRoute'
import { useState } from 'react'

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes (was cacheTime)
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AuthProvider>
          <Router>
            <div className="min-h-screen bg-gray-900 text-white">
              <Toaster
                position="top-right"
                toastOptions={{
                  className: 'bg-gray-800 text-white border border-gray-700',
                  duration: 4000,
                }}
              />

              <Routes>
                {/* Public Routes */}
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                {/* Protected Routes */}
                <Route path="/*" element={
                  <ProtectedRoute>
                    <div className="flex h-screen bg-gray-900">
                      {/* Sidebar */}
                      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />

                      {/* Main Content */}
                      <div className="flex-1 flex flex-col overflow-hidden">
                        <Navbar setSidebarOpen={setSidebarOpen} />

                        <main className="flex-1 overflow-y-auto bg-gray-900 p-4">
                          <div className="max-w-7xl mx-auto">
                            <Routes>
                              <Route path="/" element={<Navigate to="/dashboard" replace />} />
                              <Route path="/dashboard" element={<Dashboard />} />
                              <Route path="/strategies" element={<Strategies />} />
                              <Route path="/backtest" element={<Backtest />} />
                              <Route path="/portfolio" element={<Portfolio />} />
                              <Route path="/analytics" element={<Analytics />} />
                              <Route path="/defi" element={<DeFi />} />
                              <Route path="/settings" element={<Settings />} />
                            </Routes>
                          </div>
                        </main>
                      </div>
                    </div>
                  </ProtectedRoute>
                } />
              </Routes>
            </div>
          </Router>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  )
}

export default App