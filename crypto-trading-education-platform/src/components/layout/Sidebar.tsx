import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  TrendingUp,
  TestTube,
  Wallet,
  BarChart3,
  Coins,
  Settings,
  X
} from 'lucide-react'
import { cn } from '../../lib/utils'

interface SidebarProps {
  open: boolean
  setOpen: (open: boolean) => void
}

const navigation = [
  { name: 'لوحة التحكم', href: '/dashboard', icon: LayoutDashboard },
  { name: 'الاستراتيجيات', href: '/strategies', icon: TrendingUp },
  { name: 'اختبار خلفي', href: '/backtest', icon: TestTube },
  { name: 'المحفظة', href: '/portfolio', icon: Wallet },
  { name: 'التحليلات', href: '/analytics', icon: BarChart3 },
  { name: 'DeFi', href: '/defi', icon: Coins },
  { name: 'الإعدادات', href: '/settings', icon: Settings },
]

export function Sidebar({ open, setOpen }: SidebarProps) {
  const location = useLocation()

  return (
    <>
      {/* Mobile backdrop */}
      {open && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden"
          onClick={() => setOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={cn(
          'fixed inset-y-0 right-0 z-30 w-64 bg-gray-800 transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0',
          open ? 'translate-x-0' : 'translate-x-full'
        )}
      >
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <span className="text-white font-bold text-lg">TradeBot</span>
          </div>
          <button
            onClick={() => setOpen(false)}
            className="lg:hidden text-gray-400 hover:text-white"
          >
            <X size={20} />
          </button>
        </div>

        <nav className="mt-4 px-4">
          <ul className="space-y-2">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              const Icon = item.icon

              return (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    onClick={() => setOpen(false)}
                    className={cn(
                      'flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors',
                      isActive
                        ? 'bg-blue-600 text-white'
                        : 'text-gray-400 hover:text-white hover:bg-gray-700'
                    )}
                  >
                    <Icon size={18} />
                    <span>{item.name}</span>
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>

        {/* Market Summary */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-700 bg-gray-800">
          <div className="bg-gray-700 rounded-lg p-3">
            <h3 className="text-white text-sm font-medium mb-2">ملخص السوق</h3>
            <div className="space-y-1 text-xs">
              <div className="flex justify-between">
                <span className="text-gray-400">BTC:</span>
                <span className="text-green-400">$95,234 (+2.1%)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">ETH:</span>
                <span className="text-green-400">$3,456 (+1.8%)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Market Cap:</span>
                <span className="text-white">$2.1T</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}