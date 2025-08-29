import pandas as pd
import numpy as np
from .base_strategy import TradingStrategy

class RSIStrategy(TradingStrategy):
    """استراتيجية مؤشر القوة النسبية (RSI)"""

    description = "استراتيجية تعتمد على مؤشر RSI لتحديد مناطق التشبع الشرائي والبيعي"
    default_parameters = {
        'period': 14,
        'oversold': 30,
        'overbought': 70
    }

    def __init__(self, period: int = 14, oversold: float = 30, overbought: float = 70, **kwargs):
        super().__init__("RSI Strategy")
        self.period = period
        self.oversold = oversold
        self.overbought = overbought

        if self.oversold >= self.overbought:
            raise ValueError("حد التشبع البيعي يجب أن يكون أقل من حد التشبع الشرائي")

    def calculate_rsi(self, prices: pd.Series, period: int) -> pd.Series:
        """حساب مؤشر RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """توليد إشارات التداول باستخدام RSI"""
        if not self.validate_data(data):
            raise ValueError("بيانات غير صالحة")

        # حساب RSI
        rsi = self.calculate_rsi(data['close'], self.period)

        # توليد الإشارات
        signals = pd.Series(0, index=data.index)

        # إشارة شراء: عندما يعبر RSI فوق حد التشبع البيعي
        buy_signal = (rsi > self.oversold) & (rsi.shift(1) <= self.oversold)
        signals[buy_signal] = 1

        # إشارة بيع: عندما يعبر RSI تحت حد التشبع الشرائي
        sell_signal = (rsi < self.overbought) & (rsi.shift(1) >= self.overbought)
        signals[sell_signal] = -1

        # حفظ المؤشر
        self.rsi = rsi

        return signals

    def get_indicators(self) -> dict:
        """الحصول على المؤشرات المحسوبة"""
        if hasattr(self, 'rsi'):
            return {
                'RSI': self.rsi
            }
        return {}