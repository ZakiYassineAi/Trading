import React from 'react'
import { Card } from '../components/ui/card'

export function Strategies() {
  const strategies = [
    {
      id: 1,
      name: 'المتوسط المتحرك',
      description: 'استراتيجية تعتمد على متوسطات متحركة مختلفة',
      performance: '+15.2%',
      status: 'نشط',
      color: 'green'
    },
    {
      id: 2,
      name: 'RSI مع المقاومة/الدعم',
      description: 'تجمع بين مؤشر RSI ومستويات المقاومة والدعم',
      performance: '+8.7%',
      status: 'نشط',
      color: 'green'
    },
    {
      id: 3,
      name: 'Grid Trading',
      description: 'شبكة أوامر شراء وبيع في نطاقات محددة',
      performance: '+22.1%',
      status: 'جاري الاختبار',
      color: 'yellow'
    },
    {
      id: 4,
      name: 'DCA Bot',
      description: 'متوسط التكلفة بالدولار - شراء دوري',
      performance: '+5.3%',
      status: 'متوقف',
      color: 'red'
    }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">استراتيجيات التداول</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
          إضافة استراتيجية
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {strategies.map(strategy => (
          <Card key={strategy.id} className="bg-gray-800 border-gray-700 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-white">{strategy.name}</h3>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                strategy.color === 'green' ? 'bg-green-500/20 text-green-400' :
                strategy.color === 'yellow' ? 'bg-yellow-500/20 text-yellow-400' :
                'bg-red-500/20 text-red-400'
              }`}>
                {strategy.status}
              </span>
            </div>

            <p className="text-gray-400 mb-4">{strategy.description}</p>

            <div className="flex items-center justify-between">
              <div className="text-2xl font-bold text-green-400">
                {strategy.performance}
              </div>
              <div className="space-x-2">
                <button className="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm">
                  عرض
                </button>
                <button className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm">
                  تعديل
                </button>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Strategy Performance Chart */}
      <Card className="bg-gray-800 border-gray-700 p-6">
        <h2 className="text-xl font-bold text-white mb-6">أداء الاستراتيجيات</h2>
        <div className="h-80 bg-gray-900 rounded-lg flex items-center justify-center">
          <p className="text-gray-400">رسم بياني لأداء الاستراتيجيات</p>
        </div>
      </Card>
    </div>
  )
}