import React from 'react'
import { Card } from '../components/ui/card'

export function Analytics() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">تحليلات متقدمة</h1>
        <div className="flex space-x-4">
          <select className="bg-gray-700 border-gray-600 text-white px-4 py-2 rounded-lg">
            <option>آخر 24 ساعة</option>
            <option>آخر 7 أيام</option>
            <option>آخر 30 يوم</option>
            <option>آخر 3 شهور</option>
          </select>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="bg-gray-800 border-gray-700 p-6">
          <h3 className="text-lg font-medium text-gray-400 mb-2">معدل العائد اليومي</h3>
          <p className="text-3xl font-bold text-green-400">+0.85%</p>
          <p className="text-green-400 text-sm mt-1">أعلى من المتوقع</p>
        </Card>

        <Card className="bg-gray-800 border-gray-700 p-6">
          <h3 className="text-lg font-medium text-gray-400 mb-2">نسبة شارب</h3>
          <p className="text-3xl font-bold text-white">1.65</p>
          <p className="text-blue-400 text-sm mt-1">مقبولة</p>
        </Card>

        <Card className="bg-gray-800 border-gray-700 p-6">
          <h3 className="text-lg font-medium text-gray-400 mb-2">معامل التباين</h3>
          <p className="text-3xl font-bold text-yellow-400">12.3%</p>
          <p className="text-yellow-400 text-sm mt-1">متوسط المخاطر</p>
        </Card>

        <Card className="bg-gray-800 border-gray-700 p-6">
          <h3 className="text-lg font-medium text-gray-400 mb-2">معدل الربح</h3>
          <p className="text-3xl font-bold text-green-400">73%</p>
          <p className="text-green-400 text-sm mt-1">جيد جداً</p>
        </Card>
      </div>

      {/* Trading Performance */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="bg-gray-800 border-gray-700 p-6">
          <h2 className="text-xl font-bold text-white mb-6">أداء التداول</h2>
          <div className="h-64 bg-gray-900 rounded-lg flex items-center justify-center">
            <p className="text-gray-400">رسم بياني للأداء عبر الزمن</p>
          </div>
        </Card>

        <Card className="bg-gray-800 border-gray-700 p-6">
          <h2 className="text-xl font-bold text-white mb-6">توزيع العوائد</h2>
          <div className="h-64 bg-gray-900 rounded-lg flex items-center justify-center">
            <p className="text-gray-400">رسم بياني دائري للعوائد</p>
          </div>
        </Card>
      </div>

      {/* Risk Analysis */}
      <Card className="bg-gray-800 border-gray-700 p-6">
        <h2 className="text-xl font-bold text-white mb-6">تحليل المخاطر</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gray-700 p-4 rounded-lg">
            <h3 className="text-white font-medium mb-2">Value at Risk (VaR)</h3>
            <p className="text-2xl font-bold text-red-400">-2.1%</p>
            <p className="text-gray-400 text-sm">في 95% من الحالات</p>
          </div>

          <div className="bg-gray-700 p-4 rounded-lg">
            <h3 className="text-white font-medium mb-2">أقصى انخفاض</h3>
            <p className="text-2xl font-bold text-red-400">-5.8%</p>
            <p className="text-gray-400 text-sm">في آخر 30 يوم</p>
          </div>

          <div className="bg-gray-700 p-4 rounded-lg">
            <h3 className="text-white font-medium mb-2">الانتعاش المتوقع</h3>
            <p className="text-2xl font-bold text-blue-400">8.2%</p>
            <p className="text-gray-400 text-sm">في الأرباح</p>
          </div>
        </div>
      </Card>

      {/* Market Analysis */}
      <Card className="bg-gray-800 border-gray-700 p-6">
        <h2 className="text-xl font-bold text-white mb-6">تحليل السوق</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-medium text-white mb-4">مؤشرات الخوف والطمع</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Fear & Greed Index</span>
                <span className="text-yellow-400 font-medium">45 (حيادي)</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">مؤشر التقلب</span>
                <span className="text-red-400 font-medium">28 (منخفض)</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">حجم التداول</span>
                <span className="text-green-400 font-medium">142B (مرتفع)</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-medium text-white mb-4">الاتجاهات الرئيسية</h3>
            <div className="space-y-3">
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-white font-medium">Bitcoin يتجه صعوداً</p>
                <p className="text-gray-400 text-sm">مقاومة قوية عند $95,000</p>
              </div>
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-white font-medium">العملات البديلة تتبع</p>
                <p className="text-gray-400 text-sm">زيادة في الهيمنة</p>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  )
}