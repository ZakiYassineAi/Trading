import React from 'react'
import { Card } from '../components/ui/card'

export function Portfolio() {
  const holdings = [
    { symbol: 'BTC', name: 'Bitcoin', amount: '0.45231', value: '$42,130.50', change: '+2.34%', changeColor: 'text-green-400' },
    { symbol: 'ETH', name: 'Ethereum', amount: '12.8421', value: '$28,940.20', change: '+1.85%', changeColor: 'text-green-400' },
    { symbol: 'ADA', name: 'Cardano', amount: '15,420', value: '$8,210.40', change: '-0.52%', changeColor: 'text-red-400' },
    { symbol: 'DOT', name: 'Polkadot', amount: '890.21', value: '$5,830.15', change: '+3.21%', changeColor: 'text-green-400' },
    { symbol: 'LINK', name: 'Chainlink', amount: '245.80', value: '$3,420.80', change: '+0.98%', changeColor: 'text-green-400' },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">محفظة الاستثمار</h1>
        <div className="flex space-x-4">
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
            إيداع أموال
          </button>
          <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg">
            سحب أموال
          </button>
        </div>
      </div>

      {/* Portfolio Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-gray-800 border-gray-700 p-6">
          <h3 className="text-lg font-medium text-gray-400 mb-2">إجمالي قيمة المحفظة</h3>
          <p className="text-3xl font-bold text-white">$125,430.50</p>
          <p className="text-green-400 text-sm mt-1">+$3,210.75 (+2.63%)</p>
        </Card>

        <Card className="bg-gray-800 border-gray-700 p-6">
          <h3 className="text-lg font-medium text-gray-400 mb-2">الربح/الخسارة اليوم</h3>
          <p className="text-3xl font-bold text-green-400">+$1,240.30</p>
          <p className="text-green-400 text-sm mt-1">+0.99%</p>
        </Card>

        <Card className="bg-gray-800 border-gray-700 p-6">
          <h3 className="text-lg font-medium text-gray-400 mb-2">عدد العملات</h3>
          <p className="text-3xl font-bold text-white">5</p>
          <p className="text-gray-400 text-sm mt-1">عملة رقمية</p>
        </Card>
      </div>

      {/* Holdings Table */}
      <Card className="bg-gray-800 border-gray-700">
        <div className="p-6">
          <h2 className="text-xl font-bold text-white mb-6">الأصول المملوكة</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-gray-400 text-sm">
                  <th className="text-right pb-4">العملة</th>
                  <th className="text-right pb-4">الكمية</th>
                  <th className="text-right pb-4">القيمة</th>
                  <th className="text-right pb-4">التغيير 24س</th>
                  <th className="text-right pb-4">الإجراءات</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {holdings.map((holding) => (
                  <tr key={holding.symbol} className="text-white">
                    <td className="py-4">
                      <div className="flex items-center">
                        <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center mr-3">
                          <span className="text-xs font-bold">{holding.symbol[0]}</span>
                        </div>
                        <div>
                          <p className="font-medium">{holding.symbol}</p>
                          <p className="text-sm text-gray-400">{holding.name}</p>
                        </div>
                      </div>
                    </td>
                    <td className="py-4 text-right">{holding.amount}</td>
                    <td className="py-4 text-right font-medium">{holding.value}</td>
                    <td className={`py-4 text-right ${holding.changeColor}`}>{holding.change}</td>
                    <td className="py-4 text-right">
                      <div className="space-x-2">
                        <button className="text-blue-400 hover:text-blue-300 text-sm">شراء</button>
                        <button className="text-red-400 hover:text-red-300 text-sm">بيع</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </Card>

      {/* Portfolio Allocation Chart */}
      <Card className="bg-gray-800 border-gray-700 p-6">
        <h2 className="text-xl font-bold text-white mb-6">توزيع المحفظة</h2>
        <div className="h-80 bg-gray-900 rounded-lg flex items-center justify-center">
          <p className="text-gray-400">رسم بياني دائري لتوزيع المحفظة</p>
        </div>
      </Card>
    </div>
  )
}