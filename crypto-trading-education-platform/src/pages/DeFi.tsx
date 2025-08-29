import React from 'react'
import { Card } from '../components/ui/card'

export function DeFi() {
  const defiProtocols = [
    {
      name: 'Uniswap V3',
      tvl: '$6.2B',
      apy: '12.5%',
      protocol: 'DEX',
      risk: 'منخفض',
      color: 'green'
    },
    {
      name: 'Compound',
      tvl: '$3.8B',
      apy: '8.3%',
      protocol: 'Lending',
      risk: 'منخفض',
      color: 'green'
    },
    {
      name: 'Yearn Finance',
      tvl: '$850M',
      apy: '15.7%',
      protocol: 'Yield',
      risk: 'متوسط',
      color: 'yellow'
    },
    {
      name: 'Curve Finance',
      tvl: '$4.1B',
      apy: '9.8%',
      protocol: 'DEX',
      risk: 'منخفض',
      color: 'green'
    },
    {
      name: 'Balancer',
      tvl: '$1.2B',
      apy: '18.9%',
      protocol: 'DEX',
      risk: 'عالي',
      color: 'red'
    }
  ]

  const myPositions = [
    {
      protocol: 'Uniswap V3',
      pair: 'ETH/USDC',
      deposited: '$5,200',
      earned: '$780',
      apy: '15.2%'
    },
    {
      protocol: 'Compound',
      pair: 'USDT',
      deposited: '$3,000',
      earned: '$125',
      apy: '4.2%'
    }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">التمويل اللامركزي (DeFi)</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
          استكشاف الفرص
        </button>
      </div>

      {/* My DeFi Positions */}
      <Card className="bg-gray-800 border-gray-700 p-6">
        <h2 className="text-xl font-bold text-white mb-6">مراكزي في DeFi</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="bg-gray-700 p-4 rounded-lg">
            <h3 className="text-gray-400 text-sm">إجمالي المبلغ المربوط</h3>
            <p className="text-2xl font-bold text-white">$8,200</p>
          </div>
          <div className="bg-gray-700 p-4 rounded-lg">
            <h3 className="text-gray-400 text-sm">إجمالي العوائد</h3>
            <p className="text-2xl font-bold text-green-400">$905</p>
          </div>
          <div className="bg-gray-700 p-4 rounded-lg">
            <h3 className="text-gray-400 text-sm">متوسط APY</h3>
            <p className="text-2xl font-bold text-blue-400">11.8%</p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="text-gray-400 text-sm">
                <th className="text-right pb-4">البروتوكول</th>
                <th className="text-right pb-4">الزوج</th>
                <th className="text-right pb-4">المبلغ المربوط</th>
                <th className="text-right pb-4">العوائد</th>
                <th className="text-right pb-4">APY</th>
                <th className="text-right pb-4">الإجراءات</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {myPositions.map((position, index) => (
                <tr key={index} className="text-white">
                  <td className="py-4 font-medium">{position.protocol}</td>
                  <td className="py-4 text-gray-400">{position.pair}</td>
                  <td className="py-4">{position.deposited}</td>
                  <td className="py-4 text-green-400">{position.earned}</td>
                  <td className="py-4 text-blue-400">{position.apy}</td>
                  <td className="py-4">
                    <div className="space-x-2">
                      <button className="text-blue-400 hover:text-blue-300 text-sm">إدارة</button>
                      <button className="text-red-400 hover:text-red-300 text-sm">سحب</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Available DeFi Protocols */}
      <Card className="bg-gray-800 border-gray-700 p-6">
        <h2 className="text-xl font-bold text-white mb-6">البروتوكولات المتاحة</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {defiProtocols.map((protocol, index) => (
            <div key={index} className="bg-gray-700 p-4 rounded-lg">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-white font-bold">{protocol.name}</h3>
                <span className={`px-2 py-1 rounded text-xs font-medium ${
                  protocol.color === 'green' ? 'bg-green-500/20 text-green-400' :
                  protocol.color === 'yellow' ? 'bg-yellow-500/20 text-yellow-400' :
                  'bg-red-500/20 text-red-400'
                }`}>
                  {protocol.risk}
                </span>
              </div>

              <div className="space-y-2 mb-4">
                <div className="flex justify-between">
                  <span className="text-gray-400 text-sm">TVL:</span>
                  <span className="text-white text-sm">{protocol.tvl}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400 text-sm">APY:</span>
                  <span className="text-green-400 text-sm font-medium">{protocol.apy}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400 text-sm">النوع:</span>
                  <span className="text-blue-400 text-sm">{protocol.protocol}</span>
                </div>
              </div>

              <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded text-sm">
                استكشاف
              </button>
            </div>
          ))}
        </div>
      </Card>

      {/* DeFi Market Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="bg-gray-800 border-gray-700 p-6">
          <h2 className="text-xl font-bold text-white mb-6">نظرة عامة على سوق DeFi</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-400">إجمالي TVL</span>
              <span className="text-2xl font-bold text-white">$45.8B</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">التغيير 24س</span>
              <span className="text-green-400 font-medium">+3.2%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">عدد البروتوكولات</span>
              <span className="text-white font-medium">238</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">متوسط APY</span>
              <span className="text-blue-400 font-medium">12.3%</span>
            </div>
          </div>
        </Card>

        <Card className="bg-gray-800 border-gray-700 p-6">
          <h2 className="text-xl font-bold text-white mb-6">التوزيع بحسب الشبكة</h2>
          <div className="h-48 bg-gray-900 rounded-lg flex items-center justify-center">
            <p className="text-gray-400">رسم بياني دائري لتوزيع DeFi</p>
          </div>
        </Card>
      </div>
    </div>
  )
}