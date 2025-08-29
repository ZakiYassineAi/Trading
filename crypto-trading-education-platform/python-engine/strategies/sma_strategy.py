import pandas as pd
import numpy as np
from .base_strategy import TradingStrategy

class SMAStrategy(TradingStrategy):
    """استراتيجية تقاطع المتوسط المتحرك البسيط"""

    description = "استراتيجية بسيطة تعتمد على تقاطع متوسطين متحركين بسيطين"
    default_parameters = {
        'fast': 10,
        'slow': 30
    }

    def __init__(self, fast: int = 10, slow: int = 30, **kwargs):
        super().__init__("SMA Crossover Strategy")
        self.fast_period = fast
        self.slow_period = slow

        if self.fast_period >= self.slow_period:
            raise ValueError("فترة المتوسط السريع يجب أن تكون أقل من البطيء")

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """توليد إشارات التداول باستخدام SMA Crossover"""
        if not self.validate_data(data):
            raise ValueError("بيانات غير صالحة")

        # حساب المتوسطات المتحركة
        fast_sma = data['close'].rolling(window=self.fast_period).mean()
        slow_sma = data['close'].rolling(window=self.slow_period).mean()

        # توليد الإشارات
        signals = pd.Series(0, index=data.index)

        # إشارة شراء: عندما يعبر المتوسط السريع فوق البطيء
        crossover = (fast_sma > slow_sma) & (fast_sma.shift(1) <= slow_sma.shift(1))
        signals[crossover] = 1

        # إشارة بيع: عندما يعبر المتوسط السريع تحت البطيء
        crossunder = (fast_sma < slow_sma) & (fast_sma.shift(1) >= slow_sma.shift(1))
        signals[crossunder] = -1

        # حفظ المتوسطات للعرض والتحليل
        self.fast_sma = fast_sma
        self.slow_sma = slow_sma

        return signals

    def get_indicators(self) -> dict:
        """الحصول على المؤشرات المحسوبة"""
        if hasattr(self, 'fast_sma') and hasattr(self, 'slow_sma'):
            return {
                f'SMA_{self.fast_period}': self.fast_sma,
                f'SMA_{self.slow_period}': self.slow_sma
            }
        return {}