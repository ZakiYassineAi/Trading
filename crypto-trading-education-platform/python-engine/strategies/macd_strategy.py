import pandas as pd
import numpy as np
from .base_strategy import TradingStrategy

class MACDStrategy(TradingStrategy):
    """استراتيجية MACD (تقارب وتباعد المتوسطات المتحركة)"""

    description = "استراتيجية متقدمة تجمع بين مؤشرات الزخم والاتجاه باستخدام MACD"
    default_parameters = {
        'fast': 12,
        'slow': 26,
        'signal': 9
    }

    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9, **kwargs):
        super().__init__("MACD Strategy")
        self.fast_period = fast
        self.slow_period = slow
        self.signal_period = signal

        if self.fast_period >= self.slow_period:
            raise ValueError("فترة EMA السريع يجب أن تكون أقل من البطيء")

    def calculate_macd(self, prices: pd.Series) -> tuple:
        """حساب مؤشرات MACD"""
        # حساب EMA السريع والبطيء
        ema_fast = prices.ewm(span=self.fast_period, adjust=False).mean()
        ema_slow = prices.ewm(span=self.slow_period, adjust=False).mean()

        # خط MACD
        macd_line = ema_fast - ema_slow

        # خط الإشارة
        signal_line = macd_line.ewm(span=self.signal_period, adjust=False).mean()

        # الهيستوجرام
        histogram = macd_line - signal_line

        return macd_line, signal_line, histogram

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """توليد إشارات التداول باستخدام MACD"""
        if not self.validate_data(data):
            raise ValueError("بيانات غير صالحة")

        # حساب MACD
        macd_line, signal_line, histogram = self.calculate_macd(data['close'])

        # توليد الإشارات
        signals = pd.Series(0, index=data.index)

        # إشارة شراء: عندما يعبر MACD فوق خط الإشارة
        bullish_crossover = (macd_line > signal_line) & (macd_line.shift(1) <= signal_line.shift(1))
        signals[bullish_crossover] = 1

        # إشارة بيع: عندما يعبر MACD تحت خط الإشارة
        bearish_crossover = (macd_line < signal_line) & (macd_line.shift(1) >= signal_line.shift(1))
        signals[bearish_crossover] = -1

        # حفظ المؤشرات
        self.macd_line = macd_line
        self.signal_line = signal_line
        self.histogram = histogram

        return signals

    def get_indicators(self) -> dict:
        """الحصول على المؤشرات المحسوبة"""
        if all(hasattr(self, attr) for attr in ['macd_line', 'signal_line', 'histogram']):
            return {
                'MACD': self.macd_line,
                'MACD_Signal': self.signal_line,
                'MACD_Histogram': self.histogram
            }
        return {}