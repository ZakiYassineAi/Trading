import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class BacktestEngine:
    """محرك الباك-تست المتقدم لاختبار استراتيجيات التداول"""

    def __init__(self, initial_capital: float = 10000, commission: float = 0.001,
                 slippage: float = 0.0001, max_position_size: float = 0.95):
        """
        باراميترات المحرك:
        - initial_capital: رأس المال الابتدائي
        - commission: رسوم التداول (نسبة مئوية)
        - slippage: الانزلاق في التنفيذ
        - max_position_size: أقصى حجم مركز (نسبة من رأس المال)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.max_position_size = max_position_size

        # متغيرات الحالة
        self.reset()

    def reset(self):
        """إعادة تعيين حالة المحرك"""
        self.capital = self.initial_capital
        self.position = 0  # حجم المركز الحالي
        self.entry_price = 0
        self.equity_curve = []
        self.trades = []
        self.drawdown_series = []
        self.trade_count = 0

    def run(self, strategy, data: pd.DataFrame) -> Dict:
        """تشغيل باك-تست لاستراتيجية معينة"""
        self.reset()

        if data.empty or len(data) < 50:
            raise ValueError("بيانات غير كافية للباك-تست")

        print(f"بدء باك-تست على {len(data)} نقطة بيانات")

        # حساب الإشارات
        signals = strategy.generate_signals(data)

        peak_capital = self.initial_capital

        for i, row in data.iterrows():
            current_price = row['close']
            timestamp = row['timestamp']

            # الحصول على إشارة الاستراتيجية
            signal = signals.iloc[i] if i < len(signals) else 0

            # تنفيذ الصفقات
            if signal != 0 and self._can_trade(signal, current_price):
                self._execute_trade(signal, current_price, timestamp, i)

            # حساب قيمة المحفظة
            portfolio_value = self._calculate_portfolio_value(current_price)

            # تحديث أقصى قيمة
            if portfolio_value > peak_capital:
                peak_capital = portfolio_value

            # حساب الهبوط
            drawdown = (peak_capital - portfolio_value) / peak_capital * 100

            # حفظ بيانات المحفظة
            self.equity_curve.append({
                'timestamp': timestamp,
                'capital': self.capital,
                'position': self.position,
                'portfolio_value': portfolio_value,
                'drawdown': drawdown,
                'price': current_price
            })

            self.drawdown_series.append(drawdown)

        # إغلاق أي مراكز مفتوحة
        if self.position != 0:
            final_price = data.iloc[-1]['close']
            self._close_position(final_price, data.iloc[-1]['timestamp'], len(data)-1)

        print(f"انتهى الباك-تست: {len(self.trades)} صفقة")

        return {
            'final_capital': self.capital,
            'equity_curve': pd.DataFrame(self.equity_curve),
            'trades': self.trades,
            'drawdown_series': self.drawdown_series
        }

    def _can_trade(self, signal: float, price: float) -> bool:
        """التحقق من إمعان تنفيذ صفقة"""
        if signal == 0:
            return False

        # منع الصفقات المتضاربة
        if (signal > 0 and self.position > 0) or (signal < 0 and self.position < 0):
            return False

        # التحقق مع رأس المال المتاح
        if signal > 0:  # شراء
            max_shares = (self.capital * self.max_position_size) / (price * (1 + self.commission + self.slippage))
            return max_shares > 0

        return True  # بيع متاح دائماً

    def _execute_trade(self, signal: float, price: float, timestamp, index: int):
        """تنفيذ صفقة تداول"""
        # حساب سعر التنفيذ مع الانزلاق
        execution_price = price * (1 + self.slippage if signal > 0 else 1 - self.slippage)

        if signal > 0:  # إشارة شراء
            self._open_long_position(execution_price, timestamp, index)
        elif signal < 0 and self.position > 0:  # إشارة بيع (إغلاق مركز طويل)
            self._close_position(execution_price, timestamp, index)

    def _open_long_position(self, price: float, timestamp, index: int):
        """فتح مركز شراء طويل"""
        if self.position != 0:  # إغلاق المركز السابق أولاً
            self._close_position(price, timestamp, index)

        # حساب حجم المركز
        available_capital = self.capital * self.max_position_size
        total_cost_per_share = price * (1 + self.commission)

        if available_capital > total_cost_per_share:
            shares = available_capital / total_cost_per_share
            total_cost = shares * price * (1 + self.commission)

            self.position = shares
            self.entry_price = price
            self.capital -= total_cost

            # حفظ بيانات الصفقة
            self.trade_count += 1

    def _close_position(self, price: float, timestamp, index: int):
        """إغلاق المركز الحالي"""
        if self.position == 0:
            return

        # حساب العوائد/الخسائر
        sale_proceeds = self.position * price * (1 - self.commission)
        pnl = sale_proceeds - (self.position * self.entry_price * (1 + self.commission))
        pnl_percentage = (pnl / (self.position * self.entry_price)) * 100

        self.capital += sale_proceeds

        # حفظ بيانات الصفقة
        trade = {
            'id': len(self.trades) + 1,
            'entry_date': timestamp,  # سيتم تحديثه في المستقبل
            'exit_date': timestamp,
            'side': 'buy',  # long position
            'entry_price': self.entry_price,
            'exit_price': price,
            'quantity': self.position,
            'pnl': round(pnl, 2),
            'pnl_percent': round(pnl_percentage, 2),
            'fees': round(self.position * (self.entry_price + price) * self.commission, 2),
            'duration_bars': 1  # سيتم حسابه بشكل صحيح في المستقبل
        }

        self.trades.append(trade)

        # إعادة تعيين
        self.position = 0
        self.entry_price = 0

    def _calculate_portfolio_value(self, current_price: float) -> float:
        """حساب قيمة المحفظة الحالية"""
        cash = self.capital
        position_value = self.position * current_price if self.position > 0 else 0
        return cash + position_value

    def get_summary_stats(self) -> Dict:
        """الحصول على ملخص إحصائي للباك-تست"""
        if not self.equity_curve:
            return {}

        equity_df = pd.DataFrame(self.equity_curve)
        final_value = equity_df['portfolio_value'].iloc[-1]

        return {
            'initial_capital': self.initial_capital,
            'final_capital': final_value,
            'total_return': ((final_value - self.initial_capital) / self.initial_capital) * 100,
            'max_drawdown': max(self.drawdown_series) if self.drawdown_series else 0,
            'total_trades': len(self.trades),
            'winning_trades': len([t for t in self.trades if t['pnl'] > 0]),
            'losing_trades': len([t for t in self.trades if t['pnl'] < 0])
        }