import pandas as pd
import numpy as np
from .base_strategy import TradingStrategy

class ATRStrategy(TradingStrategy):
    """استراتيجية معدل المدى الحقيقي (ATR)"""

    description = "استراتيجية تعتمد على معدل المدى الحقيقي لتحديد نقاط الدخول والخروج"
    default_parameters = {
        'period': 14,
        'multiplier': 2.0
    }

    def __init__(self, period: int = 14, multiplier: float = 2.0, **kwargs):
        super().__init__("ATR Strategy")
        self.period = period
        self.multiplier = multiplier

        if self.period <= 0 or self.multiplier <= 0:
            raise ValueError("الفترة والمضاعف يجب أن يكونا أكبر من صفر")

    def calculate_atr(self, data: pd.DataFrame) -> pd.Series:
        """حساب معدل المدى الحقيقي"""
        # حساب True Range
        high_low = data['high'] - data['low']
        high_close = np.abs(data['high'] - data['close'].shift())
        low_close = np.abs(data['low'] - data['close'].shift())

        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

        # حساب ATR (متوسط True Range)
        atr = true_range.rolling(window=self.period).mean()

        return atr

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """توليد إشارات التداول باستخدام ATR"""
        if not self.validate_data(data):
            raise ValueError("بيانات غير صالحة")

        # حساب ATR
        atr = self.calculate_atr(data)

        # حساب خطوط الاتجاه
        sma = data['close'].rolling(window=self.period).mean()
        upper_band = sma + (atr * self.multiplier)
        lower_band = sma - (atr * self.multiplier)

        # توليد الإشارات
        signals = pd.Series(0, index=data.index)

        # إشارة شراء: عند اختراق الحد الأعلى
        breakout_up = (data['close'] > upper_band.shift(1)) & (data['close'].shift(1) <= upper_band.shift(2))
        signals[breakout_up] = 1

        # إشارة بيع: عند اختراق الحد الأدنى
        breakout_down = (data['close'] < lower_band.shift(1)) & (data['close'].shift(1) >= lower_band.shift(2))
        signals[breakout_down] = -1

        # حفظ المؤشرات
        self.atr = atr
        self.upper_band = upper_band
        self.lower_band = lower_band
        self.sma = sma

        return signals

    def get_indicators(self) -> dict:
        """الحصول على المؤشرات المحسوبة"""
        if all(hasattr(self, attr) for attr in ['atr', 'upper_band', 'lower_band', 'sma']):
            return {
                'ATR': self.atr,
                'ATR_Upper': self.upper_band,
                'ATR_Lower': self.lower_band,
                'ATR_Middle': self.sma
            }
        return {}