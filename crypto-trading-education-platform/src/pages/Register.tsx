import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Card } from '../components/ui/card'
import { useAuth } from '../contexts/AuthContext'

export function Register() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (password !== confirmPassword) {
      alert('كلمات المرور غير متطابقة')
      return
    }

    setLoading(true)

    try {
      await register(email, password, fullName)
      navigate('/dashboard')
    } catch (error) {
      console.error('Registration error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
      <Card className="w-full max-w-md bg-gray-800 border-gray-700 p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">إنشاء حساب جديد</h1>
          <p className="text-gray-400">انضم إلى منصة التداول الاحترافية</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              الاسم الكامل
            </label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full px-3 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="أدخل اسمك الكامل"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              البريد الإلكتروني
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="أدخل بريدك الإلكتروني"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              كلمة المرور
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="أدخل كلمة المرور"
              required
              minLength={6}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              تأكيد كلمة المرور
            </label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-3 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="أعد إدخال كلمة المرور"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-medium py-3 px-4 rounded-lg transition-colors"
          >
            {loading ? 'جاري إنشاء الحساب...' : 'إنشاء حساب'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-400">
            لديك حساب بالفعل؟{' '}
            <Link to="/login" className="text-blue-400 hover:text-blue-300 font-medium">
              سجل دخولك
            </Link>
          </p>
        </div>
      </Card>
    </div>
  )
}