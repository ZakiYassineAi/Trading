import React from 'react'
import { Bell, User, Settings, LogOut, Menu } from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'

interface NavbarProps {
  setSidebarOpen: (open: boolean) => void
}

export function Navbar({ setSidebarOpen }: NavbarProps) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <header className="bg-gray-800 border-b border-gray-700 px-4 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setSidebarOpen(true)}
            className="lg:hidden text-gray-400 hover:text-white"
          >
            <Menu size={24} />
          </button>
          <div className="text-white">
            <h1 className="text-xl font-bold">منصة التداول الاحترافية</h1>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {/* Market Status */}
          <div className="hidden md:flex items-center space-x-2">
            <div className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm">
              <span className="w-2 h-2 bg-green-500 rounded-full inline-block mr-2"></span>
              السوق مفتوح
            </div>
          </div>

          {/* Notifications */}
          <button className="relative text-gray-400 hover:text-white">
            <Bell size={20} />
            <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center">
              3
            </span>
          </button>

          {/* User Menu */}
          <div className="relative group">
            <button className="flex items-center space-x-2 text-gray-400 hover:text-white">
              <User size={20} />
              <span className="hidden md:inline text-sm">{user?.email}</span>
            </button>

            <div className="absolute left-0 mt-2 w-48 bg-gray-800 rounded-lg shadow-lg border border-gray-700 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
              <div className="py-1">
                <button
                  onClick={() => navigate('/settings')}
                  className="flex items-center space-x-2 w-full text-right px-4 py-2 text-sm text-gray-400 hover:text-white hover:bg-gray-700"
                >
                  <Settings size={16} />
                  <span>الإعدادات</span>
                </button>
                <hr className="border-gray-700" />
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-2 w-full text-right px-4 py-2 text-sm text-gray-400 hover:text-white hover:bg-gray-700"
                >
                  <LogOut size={16} />
                  <span>تسجيل الخروج</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}