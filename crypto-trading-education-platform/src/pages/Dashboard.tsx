import React from 'react'
import { Card } from '../components/ui/card'
import RiskWarning from '@/components/ui/RiskWarning'

export function Dashboard() {
  return (
    <div className="space-y-6">
      <RiskWarning />
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">لوحة التداول الاحترافية</h1>
        <div className="flex items-center space-x-4">
          <div className="bg-green-500/20 text-green-400 px-3 py-1 rounded-lg text-sm font-medium">
            السوق مفتوح
          </div>
        </div>
      </div>

      {/* Portfolio Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="bg-gray-800 border-gray-700 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">إجمالي المحفظة</p>
              <p className="text-2xl font-bold text-white">$125,430.50</p>
              <p className="text-green-400 text-sm">+2.5% اليوم</p>
            </div>
          </div>
        </Card>

        <Card className="bg-gray-800 border-gray-700 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">الربح/الخسارة</p>
              <p className="text-2xl font-bold text-green-400">+$3,210.75</p>
              <p className="text-green-400 text-sm">+2.63% كل الأوقات</p>
            </div>
          </div>
        </Card>

        <Card className="bg-gray-800 border-gray-700 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">النقد المتاح</p>
              <p className="text-2xl font-bold text-white">$45,230.20</p>
              <p className="text-gray-400 text-sm">USD</p>
            </div>
          </div>
        </Card>

        <Card className="bg-gray-800 border-gray-700 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">عدد الصفقات النشطة</p>
              <p className="text-2xl font-bold text-blue-400">7</p>
              <p className="text-gray-400 text-sm">منها 5 مربحة</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Main Trading Interface */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trading Chart */}
        <div className="lg:col-span-2">
          <Card className="bg-gray-800 border-gray-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">الرسم البياني للتداول</h2>
            <div className="h-96 bg-gray-900 rounded-lg flex items-center justify-center">
              <p className="text-gray-400">TradingView Chart سيتم تحميله هنا</p>
            </div>
          </Card>
        </div>

        {/* Order Book & Trade Form */}
        <div className="space-y-6">
          <Card className="bg-gray-800 border-gray-700 p-6">
            <h3 className="text-lg font-bold text-white mb-4">نموذج الطلبات</h3>
            <div className="space-y-4">
              <div>
                <label className="text-sm text-gray-400">نوع الطلب</label>
                <select className="w-full mt-1 bg-gray-700 border-gray-600 rounded-lg p-3 text-white">
                  <option>طلب فوري</option>
                  <option>طلب محدود</option>
                </select>
              </div>
              <div>
                <label className="text-sm text-gray-400">الكمية</label>
                <input type="number" className="w-full mt-1 bg-gray-700 border-gray-600 rounded-lg p-3 text-white" placeholder="0.00" />
              </div>
              <div>
                <label className="text-sm text-gray-400">السعر</label>
                <input type="number" className="w-full mt-1 bg-gray-700 border-gray-600 rounded-lg p-3 text-white" placeholder="0.00" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <button className="bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-medium">
                  شراء
                </button>
                <button className="bg-red-600 hover:bg-red-700 text-white py-3 rounded-lg font-medium">
                  بيع
                </button>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}