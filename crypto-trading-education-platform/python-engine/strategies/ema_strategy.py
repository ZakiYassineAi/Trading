import pandas as pd
import numpy as np
from .base_strategy import TradingStrategy

class EMAStrategy(TradingStrategy):
    """استراتيجية تقاطع المتوسط المتحرك الأسي"""

    description = "استراتيجية متقدمة تعتمد على تقاطع المتوسطات المتحركة الأسية"
    default_parameters = {
        'fast': 12,
        'slow': 26
    }

    def __init__(self, fast: int = 12, slow: int = 26, **kwargs):
        super().__init__("EMA Crossover Strategy")
        self.fast_period = fast
        self.slow_period = slow

        if self.fast_period >= self.slow_period:
            raise ValueError("فترة EMA السريع يجب أن تكون أقل من البطيء")

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """توليد إشارات التداول باستخدام EMA Crossover"""
        if not self.validate_data(data):
            raise ValueError("بيانات غير صالحة")

        # حساب المتوسطات المتحركة الأسية
        fast_ema = data['close'].ewm(span=self.fast_period, adjust=False).mean()
        slow_ema = data['close'].ewm(span=self.slow_period, adjust=False).mean()

        # توليد الإشارات
        signals = pd.Series(0, index=data.index)

        # إشارة شراء: عندما يعبر EMA السريع فوق البطيء
        crossover = (fast_ema > slow_ema) & (fast_ema.shift(1) <= slow_ema.shift(1))
        signals[crossover] = 1

        # إشارة بيع: عندما يعبر EMA السريع تحت البطيء
        crossunder = (fast_ema < slow_ema) & (fast_ema.shift(1) >= slow_ema.shift(1))
        signals[crossunder] = -1

        # حفظ المتوسطات
        self.fast_ema = fast_ema
        self.slow_ema = slow_ema

        return signals

    def get_indicators(self) -> dict:
        """الحصول على المؤشرات المحسوبة"""
        if hasattr(self, 'fast_ema') and hasattr(self, 'slow_ema'):
            return {
                f'EMA_{self.fast_period}': self.fast_ema,
                f'EMA_{self.slow_period}': self.slow_ema
            }
        return {}