import pandas as pd
import numpy as np
from .base_strategy import TradingStrategy

class VolatilityTargetingStrategy(TradingStrategy):
    """استراتيجية استهداف التقلبات"""

    description = "استراتيجية متقدمة تضبط حجم المراكز بناءً على مستوى التقلبات"
    default_parameters = {
        'target_volatility': 0.15,  # 15% target volatility
        'vol_period': 20,
        'rebalance_frequency': 5,
        'trend_period': 50
    }

    def __init__(self, target_volatility: float = 0.15, vol_period: int = 20,
                 rebalance_frequency: int = 5, trend_period: int = 50, **kwargs):
        super().__init__("Volatility Targeting Strategy")
        self.target_volatility = target_volatility
        self.vol_period = vol_period
        self.rebalance_frequency = rebalance_frequency
        self.trend_period = trend_period

        if any(x <= 0 for x in [self.target_volatility, self.vol_period, self.rebalance_frequency, self.trend_period]):
            raise ValueError("جميع المعاملات يجب أن تكون أكبر من صفر")

    def calculate_volatility(self, prices: pd.Series) -> pd.Series:
        """حساب التقلبات المتحركة"""
        returns = prices.pct_change().dropna()
        volatility = returns.rolling(window=self.vol_period).std() * np.sqrt(252)  # Annualized
        return volatility

    def calculate_position_size(self, current_volatility: float) -> float:
        """حساب حجم المركز بناءً على التقلبات"""
        if current_volatility <= 0:
            return 0

        # حساب نسبة التقلبات المستهدفة إلى الحالية
        vol_ratio = self.target_volatility / current_volatility

        # حدود حجم المركز (من 0.1 إلى 2.0)
        position_size = np.clip(vol_ratio, 0.1, 2.0)

        return position_size

    def calculate_trend_signal(self, prices: pd.Series) -> pd.Series:
        """حساب إشارة الاتجاه"""
        # استخدام متوسط متحرك بسيط لتحديد الاتجاه
        sma = prices.rolling(window=self.trend_period).mean()

        # 1 = uptrend, -1 = downtrend, 0 = sideways
        trend = pd.Series(0, index=prices.index)
        trend[prices > sma * 1.02] = 1   # 2% فوق المتوسط
        trend[prices < sma * 0.98] = -1  # 2% تحت المتوسط

        return trend, sma

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """توليد إشارات التداول باستخدام Volatility Targeting"""
        if not self.validate_data(data):
            raise ValueError("بيانات غير صالحة")

        # حساب التقلبات
        volatility = self.calculate_volatility(data['close'])

        # حساب إشارة الاتجاه
        trend_signal, trend_sma = self.calculate_trend_signal(data['close'])

        # حساب أحجام المراكز
        position_sizes = volatility.apply(self.calculate_position_size)

        # توليد إشارات معدلة بحجم المركز
        base_signals = trend_signal * position_sizes

        # إعادة موازنة دورية
        signals = pd.Series(0.0, index=data.index)

        for i in range(len(data)):
            if i % self.rebalance_frequency == 0:  # إعادة موازنة كل N فترات
                current_signal = base_signals.iloc[i]

                # تطبيق فلاتر لتجنب التغيرات الصغيرة
                if abs(current_signal) > 0.1:  # حد أدنى للإشارة
                    signals.iloc[i] = current_signal

        # حفظ المؤشرات
        self.volatility = volatility
        self.trend_signal = trend_signal
        self.trend_sma = trend_sma
        self.position_sizes = position_sizes

        # تحويل إلى إشارات بسيطة (1, 0, -1)
        discrete_signals = pd.Series(0, index=data.index)
        discrete_signals[signals > 0.3] = 1
        discrete_signals[signals < -0.3] = -1

        return discrete_signals

    def get_indicators(self) -> dict:
        """الحصول على المؤشرات المحسوبة"""
        if all(hasattr(self, attr) for attr in ['volatility', 'trend_signal', 'trend_sma', 'position_sizes']):
            return {
                'Volatility': self.volatility,
                'Trend_Signal': self.trend_signal,
                'Trend_SMA': self.trend_sma,
                'Position_Size': self.position_sizes
            }
        return {}