import React from 'react'
import { Card } from '../components/ui/card'

export function Settings() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">الإعدادات</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Account Settings */}
        <Card className="bg-gray-800 border-gray-700 p-6">
          <h2 className="text-xl font-bold text-white mb-6">إعدادات الحساب</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                الاسم الكامل
              </label>
              <input
                type="text"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                defaultValue="محمد أحمد"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                البريد الإلكتروني
              </label>
              <input
                type="email"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                defaultValue="mohammed.ahmed@example.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                رقم الهاتف
              </label>
              <input
                type="tel"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                defaultValue="+966 50 123 4567"
              />
            </div>
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
              حفظ التغييرات
            </button>
          </div>
        </Card>

        {/* Security Settings */}
        <Card className="bg-gray-800 border-gray-700 p-6">
          <h2 className="text-xl font-bold text-white mb-6">إعدادات الأمان</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-700 rounded-lg">
              <div>
                <h3 className="text-white font-medium">المصادقة الثنائية (2FA)</h3>
                <p className="text-gray-400 text-sm">حماية إضافية لحسابك</p>
              </div>
              <div className="flex items-center">
                <input type="checkbox" className="toggle" defaultChecked />
              </div>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-700 rounded-lg">
              <div>
                <h3 className="text-white font-medium">إشعارات التسجيل</h3>
                <p className="text-gray-400 text-sm">إشعار عند تسجيل الدخول</p>
              </div>
              <div className="flex items-center">
                <input type="checkbox" className="toggle" defaultChecked />
              </div>
            </div>

            <button className="w-full bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg">
              تغيير كلمة المرور
            </button>
          </div>
        </Card>

        {/* Trading Settings */}
        <Card className="bg-gray-800 border-gray-700 p-6">
          <h2 className="text-xl font-bold text-white mb-6">إعدادات التداول</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                وضع التداول
              </label>
              <select className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white">
                <option>تجريبي (Paper Trading)</option>
                <option>حقيقي (Live Trading)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                حد المخاطرة اليومي
              </label>
              <input
                type="number"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                defaultValue="5"
                min="1"
                max="50"
              />
              <p className="text-xs text-gray-400 mt-1">% من إجمالي المحفظة</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Stop Loss افتراضي
              </label>
              <input
                type="number"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                defaultValue="2"
                min="0.5"
                max="10"
                step="0.1"
              />
              <p className="text-xs text-gray-400 mt-1">%</p>
            </div>
          </div>
        </Card>

        {/* Notifications */}
        <Card className="bg-gray-800 border-gray-700 p-6">
          <h2 className="text-xl font-bold text-white mb-6">الإشعارات</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-700 rounded-lg">
              <div>
                <h3 className="text-white font-medium">إشعارات البريد</h3>
                <p className="text-gray-400 text-sm">تقارير يومية وأخبار</p>
              </div>
              <input type="checkbox" className="toggle" defaultChecked />
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-700 rounded-lg">
              <div>
                <h3 className="text-white font-medium">إشعارات دفع</h3>
                <p className="text-gray-400 text-sm">إشعارات فورية للتداولات</p>
              </div>
              <input type="checkbox" className="toggle" defaultChecked />
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-700 rounded-lg">
              <div>
                <h3 className="text-white font-medium">إشعارات SMS</h3>
                <p className="text-gray-400 text-sm">إشعارات مهمة فقط</p>
              </div>
              <input type="checkbox" className="toggle" />
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}