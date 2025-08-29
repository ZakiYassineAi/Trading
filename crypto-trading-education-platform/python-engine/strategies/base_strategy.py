import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

class TradingStrategy(ABC):
    """فئة أساسية لجميع استراتيجيات التداول"""

    def __init__(self, name: str = "Base Strategy"):
        self.name = name
        self.signals = pd.Series()

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """توليد إشارات التداول

        Args:
            data: بيانات OHLCV

        Returns:
            pd.Series: إشارات (1 = شراء, -1 = بيع, 0 = لا عمل)
        """
        pass

    def validate_data(self, data: pd.DataFrame) -> bool:
        """التحقق من صحة البيانات"""
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        return all(col in data.columns for col in required_columns)

    def get_strategy_info(self) -> dict:
        """معلومات الاستراتيجية"""
        return {
            'name': self.name,
            'type': self.__class__.__name__,
            'description': getattr(self, 'description', 'لا يوجد وصف')
        }