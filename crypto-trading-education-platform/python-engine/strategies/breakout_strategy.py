import pandas as pd
import numpy as np
from .base_strategy import TradingStrategy

class BreakoutStrategy(TradingStrategy):
    """استراتيجية اختراق المقاومات والدعم"""

    description = "استراتيجية تعتمد على اختراق مستويات المقاومة والدعم المحددة باستخدام القنوات"
    default_parameters = {
        'period': 20,
        'breakout_factor': 1.02  # 2% breakout threshold
    }

    def __init__(self, period: int = 20, breakout_factor: float = 1.02, **kwargs):
        super().__init__("Breakout Strategy")
        self.period = period
        self.breakout_factor = breakout_factor

        if self.period <= 0:
            raise ValueError("فترة الحساب يجب أن تكون أكبر من صفر")

    def calculate_channels(self, data: pd.DataFrame) -> tuple:
        """حساب قنوات التداول"""
        # حساب الحد الأعلى والأدنى لفترة معينة
        upper_channel = data['high'].rolling(window=self.period).max()
        lower_channel = data['low'].rolling(window=self.period).min()
        middle_channel = (upper_channel + lower_channel) / 2

        return upper_channel, lower_channel, middle_channel

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """توليد إشارات التداول باستخدام Breakout"""
        if not self.validate_data(data):
            raise ValueError("بيانات غير صالحة")

        # حساب القنوات
        upper_channel, lower_channel, middle_channel = self.calculate_channels(data)

        # توليد الإشارات
        signals = pd.Series(0, index=data.index)

        # إشارة شراء: عند اختراق الحد الأعلى مع حجم تداول عالي
        breakout_up = (
            (data['close'] > upper_channel.shift(1) * self.breakout_factor) &
            (data['close'].shift(1) <= upper_channel.shift(2)) &
            (data['volume'] > data['volume'].rolling(window=self.period).mean())
        )
        signals[breakout_up] = 1

        # إشارة بيع: عند اختراق الحد الأدنى مع حجم تداول عالي
        breakout_down = (
            (data['close'] < lower_channel.shift(1) / self.breakout_factor) &
            (data['close'].shift(1) >= lower_channel.shift(2)) &
            (data['volume'] > data['volume'].rolling(window=self.period).mean())
        )
        signals[breakout_down] = -1

        # حفظ القنوات
        self.upper_channel = upper_channel
        self.lower_channel = lower_channel
        self.middle_channel = middle_channel

        return signals

    def get_indicators(self) -> dict:
        """الحصول على المؤشرات المحسوبة"""
        if all(hasattr(self, attr) for attr in ['upper_channel', 'lower_channel', 'middle_channel']):
            return {
                'Upper_Channel': self.upper_channel,
                'Lower_Channel': self.lower_channel,
                'Middle_Channel': self.middle_channel
            }
        return {}