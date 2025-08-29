import React from 'react'
import { Card } from '../components/ui/card'

export function Backtest() {
  const backtestResults = [
    {
      id: 1,
      strategy: 'المتوسط المتحرك',
      period: '2024-01-01 إلى 2024-12-01',
      totalReturn: '15.2%',
      maxDrawdown: '-3.2%',
      winRate: '68%',
      trades: 145
    },
    {
      id: 2,
      strategy: 'RSI مع المقاومة/الدعم',
      period: '2024-01-01 إلى 2024-12-01',
      totalReturn: '22.8%',
      maxDrawdown: '-5.1%',
      winRate: '71%',
      trades: 98
    },
    {
      id: 3,
      strategy: 'Grid Trading',
      period: '2024-06-01 إلى 2024-12-01',
      totalReturn: '31.5%',
      maxDrawdown: '-2.8%',
      winRate: '78%',
      trades: 234
    }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">اختبار الاستراتيجيات</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
          اختبار جديد
        </button>
      </div>

      {/* Backtest Configuration */}
      <Card className="bg-gray-800 border-gray-700 p-6">
        <h2 className="text-xl font-bold text-white mb-6">إعداد الاختبار</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              الاستراتيجية
            </label>
            <select className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white">
              <option>المتوسط المتحرك</option>
              <option>RSI مع المقاومة/الدعم</option>
              <option>Grid Trading</option>
              <option>DCA Bot</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              العملة الرقمية
            </label>
            <select className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white">
              <option>BTC/USDT</option>
              <option>ETH/USDT</option>
              <option>ADA/USDT</option>
              <option>DOT/USDT</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              الرأسمال البداية
            </label>
            <input
              type="number"
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
              placeholder="10000"
              defaultValue="10000"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              تاريخ البداية
            </label>
            <input
              type="date"
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
              defaultValue="2024-01-01"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              تاريخ النهاية
            </label>
            <input
              type="date"
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
              defaultValue="2024-12-01"
            />
          </div>
        </div>

        <div className="mt-6">
          <button className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg">
            بدء الاختبار
          </button>
        </div>
      </Card>

      {/* Backtest Results */}
      <Card className="bg-gray-800 border-gray-700">
        <div className="p-6">
          <h2 className="text-xl font-bold text-white mb-6">نتائج الاختبارات السابقة</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-gray-400 text-sm">
                  <th className="text-right pb-4">الاستراتيجية</th>
                  <th className="text-right pb-4">الفترة</th>
                  <th className="text-right pb-4">إجمالي العائد</th>
                  <th className="text-right pb-4">أقصى انخفاض</th>
                  <th className="text-right pb-4">معدل الربح</th>
                  <th className="text-right pb-4">عدد الصفقات</th>
                  <th className="text-right pb-4">الإجراءات</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {backtestResults.map((result) => (
                  <tr key={result.id} className="text-white">
                    <td className="py-4 font-medium">{result.strategy}</td>
                    <td className="py-4 text-gray-400">{result.period}</td>
                    <td className="py-4 text-green-400 font-medium">{result.totalReturn}</td>
                    <td className="py-4 text-red-400">{result.maxDrawdown}</td>
                    <td className="py-4 text-blue-400">{result.winRate}</td>
                    <td className="py-4">{result.trades}</td>
                    <td className="py-4">
                      <div className="space-x-2">
                        <button className="text-blue-400 hover:text-blue-300 text-sm">عرض</button>
                        <button className="text-green-400 hover:text-green-300 text-sm">تطبيق</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </Card>

      {/* Performance Chart */}
      <Card className="bg-gray-800 border-gray-700 p-6">
        <h2 className="text-xl font-bold text-white mb-6">منحنى الأداء</h2>
        <div className="h-80 bg-gray-900 rounded-lg flex items-center justify-center">
          <p className="text-gray-400">رسم بياني لأداء الاستراتيجية عبر الزمن</p>
        </div>
      </Card>
    </div>
  )
}