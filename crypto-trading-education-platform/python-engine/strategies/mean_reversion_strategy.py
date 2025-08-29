import pandas as pd
import numpy as np
from .base_strategy import TradingStrategy

class MeanReversionStrategy(TradingStrategy):
    """استراتيجية العودة إلى المتوسط"""

    description = "استراتيجية تفترض أن الأسعار ستعود إلى متوسطها التاريخي بعد حركات قوية"
    default_parameters = {
        'period': 20,
        'std_dev': 2.0,
        'rsi_period': 14,
        'rsi_oversold': 30,
        'rsi_overbought': 70
    }

    def __init__(self, period: int = 20, std_dev: float = 2.0,
                 rsi_period: int = 14, rsi_oversold: float = 30,
                 rsi_overbought: float = 70, **kwargs):
        super().__init__("Mean Reversion Strategy")
        self.period = period
        self.std_dev = std_dev
        self.rsi_period = rsi_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought

        if self.period <= 0 or self.std_dev <= 0:
            raise ValueError("الفترة والانحراف المعياري يجب أن يكونا أكبر من صفر")

    def calculate_bollinger_bands(self, prices: pd.Series) -> tuple:
        """حساب Bollinger Bands"""
        sma = prices.rolling(window=self.period).mean()
        std = prices.rolling(window=self.period).std()

        upper_band = sma + (std * self.std_dev)
        lower_band = sma - (std * self.std_dev)

        return upper_band, sma, lower_band

    def calculate_rsi(self, prices: pd.Series) -> pd.Series:
        """حساب RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """توليد إشارات التداول باستخدام Mean Reversion"""
        if not self.validate_data(data):
            raise ValueError("بيانات غير صالحة")

        # حساب Bollinger Bands
        bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(data['close'])

        # حساب RSI
        rsi = self.calculate_rsi(data['close'])

        # حساب مؤشر الموضع نسبة إلى النطاق
        bb_position = (data['close'] - bb_lower) / (bb_upper - bb_lower)

        # توليد الإشارات
        signals = pd.Series(0, index=data.index)

        # إشارة شراء: عند الوصول للحد الأدنى + RSI oversold
        oversold_condition = (
            (data['close'] <= bb_lower) &  # لمس الحد الأدنى
            (rsi <= self.rsi_oversold) &   # RSI في منطقة التشبع البيعي
            (bb_position <= 0.1)           # بالقرب من الحد الأدنى
        )
        signals[oversold_condition] = 1

        # إشارة بيع: عند الوصول للحد الأعلى + RSI overbought
        overbought_condition = (
            (data['close'] >= bb_upper) &  # لمس الحد الأعلى
            (rsi >= self.rsi_overbought) & # RSI في منطقة التشبع الشرائي
            (bb_position >= 0.9)           # بالقرب من الحد الأعلى
        )
        signals[overbought_condition] = -1

        # إشارة إغلاق: عودة السعر قريباً من المتوسط
        close_to_mean = (
            (np.abs(data['close'] - bb_middle) / bb_middle <= 0.01) &  # 1% من المتوسط
            (bb_position >= 0.4) & (bb_position <= 0.6)  # في الوسط
        )

        # حفظ المؤشرات
        self.bb_upper = bb_upper
        self.bb_middle = bb_middle
        self.bb_lower = bb_lower
        self.rsi = rsi
        self.bb_position = bb_position

        return signals

    def get_indicators(self) -> dict:
        """الحصول على المؤشرات المحسوبة"""
        if all(hasattr(self, attr) for attr in ['bb_upper', 'bb_middle', 'bb_lower', 'rsi']):
            return {
                'BB_Upper': self.bb_upper,
                'BB_Middle': self.bb_middle,
                'BB_Lower': self.bb_lower,
                'RSI': self.rsi,
                'BB_Position': self.bb_position
            }
        return {}