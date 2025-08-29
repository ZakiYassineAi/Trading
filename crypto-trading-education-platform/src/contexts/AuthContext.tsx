import React, { createContext, useContext, useEffect, useState } from 'react'
import { apiClient } from '../lib/api'
import toast from 'react-hot-toast'

interface User {
  id: string
  username: string
  email: string
  fullName: string
  preferences: {
    language: string
    currency: string
    timezone: string
  }
  paperTradingOnly: boolean
  liveTradingDisabled: boolean
}

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, fullName: string) => Promise<void>
  logout: () => void
  updateUser: (updates: Partial<User>) => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  // Load user on mount
  useEffect(() => {
    loadUser()
  }, [])

  const loadUser = async () => {
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        setLoading(false)
        return
      }

      const response = await apiClient.get('/auth/me')
      setUser(response.data.user)
    } catch (error: any) {
      console.error('خطأ في تحميل المستخدم:', error)
      localStorage.removeItem('token')
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/auth/login', { email, password })
      const { token, user } = response.data

      localStorage.setItem('token', token)
      setUser(user)

      toast.success(`مرحباً ${user.fullName || user.email}! تم تسجيل الدخول بنجاح`)
    } catch (error: any) {
      const message = error.response?.data?.error || 'حدث خطأ في تسجيل الدخول'
      toast.error(message)
      throw error
    }
  }

  const register = async (email: string, password: string, fullName: string) => {
    try {
      const response = await apiClient.post('/auth/register', { email, password, fullName })

      toast.success('تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول')

      // Auto login after successful registration
      await login(email, password)
    } catch (error: any) {
      const message = error.response?.data?.error || 'حدث خطأ في إنشاء الحساب'
      toast.error(message)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
    toast.success('تم تسجيل الخروج بنجاح')
  }

  const updateUser = (updates: Partial<User>) => {
    if (user) {
      setUser({ ...user, ...updates })
    }
  }

  return (
    <AuthContext.Provider value={{
      user,
      loading,
      login,
      register,
      logout,
      updateUser
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}