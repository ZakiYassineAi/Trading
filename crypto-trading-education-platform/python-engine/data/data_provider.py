import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import time
import ta
from typing import Dict, List, Optional
import json

class DataProvider:
    """مزود البيانات المالية للعملات الرقمية"""

    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.cache = {}

    def get_data(self, symbol: str, start_date: str, end_date: str, timeframe: str = '1d') -> pd.DataFrame:
        """الحصول على البيانات التاريخية لعملة معينة"""
        try:
            # محاولة الحصول على بيانات حقيقية من CoinGecko
            real_data = self._fetch_from_coingecko(symbol, start_date, end_date)
            if not real_data.empty:
                return self._process_data(real_data, timeframe)
        except Exception as e:
            print(f"فشل في جلب البيانات الحقيقية: {e}")

        # في حالة فشل API، توليد بيانات محاكاة
        return self._generate_mock_data(symbol, start_date, end_date, timeframe)

    def _fetch_from_coingecko(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """جلب البيانات من CoinGecko API"""
        # تحويل رمز العملة إلى id المطلوب
        coin_id = self._get_coin_id(symbol)
        if not coin_id:
            raise Exception(f"لم يتم العثور على العملة: {symbol}")

        # حساب عدد الأيام
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        days = (end - start).days

        url = f"{self.base_url}/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': days,
            'interval': 'daily'
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # تحويل البيانات إلى DataFrame
        prices = data['prices']
        volumes = data['total_volumes']
        market_caps = data['market_caps']

        df = pd.DataFrame({
            'timestamp': [datetime.fromtimestamp(p[0]/1000) for p in prices],
            'price': [p[1] for p in prices],
            'volume': [v[1] for v in volumes],
            'market_cap': [mc[1] for mc in market_caps]
        })

        return df

    def _get_coin_id(self, symbol: str) -> Optional[str]:
        """تحويل رمز العملة إلى coin_id الخاص بـ CoinGecko"""
        symbol_mapping = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'ADA': 'cardano',
            'MATIC': 'matic-network',
            'LINK': 'chainlink',
            'SOL': 'solana',
            'AVAX': 'avalanche-2',
            'DOT': 'polkadot'
        }

        return symbol_mapping.get(symbol.upper(), symbol.lower())

    def _generate_mock_data(self, symbol: str, start_date: str, end_date: str, timeframe: str) -> pd.DataFrame:
        """توليد بيانات محاكاة واقعية"""
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        # تحديد الفترة الزمنية
        if timeframe == '1h':
            freq = 'H'
            periods = int((end - start).total_seconds() / 3600)
        else:  # 1d
            freq = 'D'
            periods = (end - start).days + 1

        dates = pd.date_range(start=start, periods=periods, freq=freq)

        # تحديد السعر الأساسي بناءً على العملة
        base_prices = {
            'BTC': 45000,
            'ETH': 3200,
            'ADA': 0.52,
            'MATIC': 0.95,
            'LINK': 18.5,
            'SOL': 95,
            'AVAX': 42,
            'DOT': 7.8
        }

        base_price = base_prices.get(symbol.upper(), 100)

        # توليد بيانات OHLC واقعية باستخدام Geometric Brownian Motion
        np.random.seed(42)  # للحصول على نتائج ثابتة

        # معاملات النموذج
        mu = 0.0002  # معدل النمو اليومي
        sigma = 0.02  # التقلبات

        # توليد التغيرات العشوائية
        dt = 1.0
        if timeframe == '1h':
            dt = 1.0/24  # تعديل للساعات
            sigma = sigma / np.sqrt(24)  # تعديل التقلبات للساعات

        # توليد المسار العشوائي
        dW = np.random.normal(0, np.sqrt(dt), periods)
        price_changes = mu * dt + sigma * dW

        # حساب الأسعار
        log_prices = np.log(base_price) + np.cumsum(price_changes)
        close_prices = np.exp(log_prices)

        # توليد OHLC من أسعار الإغلاق
        data = []
        for i, (date, close) in enumerate(zip(dates, close_prices)):
            if i == 0:
                open_price = base_price
            else:
                open_price = close_prices[i-1]

            # إضافة تقلبات داخل اليوم
            high_factor = 1 + abs(np.random.normal(0, 0.01))
            low_factor = 1 - abs(np.random.normal(0, 0.01))

            high = max(open_price, close) * high_factor
            low = min(open_price, close) * low_factor

            # توليد حجم التداول
            volume = np.random.lognormal(15, 1) * (base_price / 1000)

            data.append({
                'timestamp': date,
                'open': round(open_price, 8),
                'high': round(high, 8),
                'low': round(low, 8),
                'close': round(close, 8),
                'volume': round(volume, 0)
            })

        df = pd.DataFrame(data)
        return self._process_data(df, timeframe)

    def _process_data(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """معالجة وتنظيف البيانات"""
        # التأكد من وجود الأعمدة المطلوبة
        if 'open' not in df.columns and 'price' in df.columns:
            # إنشاء OHLC من بيانات الأسعار البسيطة
            df = self._create_ohlc_from_price(df)

        # ترتيب البيانات حسب التاريخ
        df = df.sort_values('timestamp').reset_index(drop=True)

        # حساب المؤشرات الفنية الأساسية
        df = self.calculate_technical_indicators(df)

        return df

    def _create_ohlc_from_price(self, df: pd.DataFrame) -> pd.DataFrame:
        """إنشاء بيانات OHLC من أسعار بسيطة"""
        new_data = []

        for i, row in df.iterrows():
            price = row['price']
            # إضافة تقلبات بسيطة
            volatility = price * 0.01

            open_price = price + np.random.normal(0, volatility/2)
            high = price + abs(np.random.normal(0, volatility))
            low = price - abs(np.random.normal(0, volatility))
            close = price

            new_data.append({
                'timestamp': row['timestamp'],
                'open': max(0, open_price),
                'high': max(open_price, close, high),
                'low': min(open_price, close, low),
                'close': close,
                'volume': row.get('volume', 1000000)
            })

        return pd.DataFrame(new_data)

    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """حساب المؤشرات الفنية"""
        try:
            # المتوسطات المتحركة
            df['sma_10'] = ta.trend.sma_indicator(df['close'], window=10)
            df['sma_30'] = ta.trend.sma_indicator(df['close'], window=30)
            df['ema_12'] = ta.trend.ema_indicator(df['close'], window=12)
            df['ema_26'] = ta.trend.ema_indicator(df['close'], window=26)

            # مؤشر القوة النسبية
            df['rsi'] = ta.momentum.rsi(df['close'], window=14)

            # MACD
            macd = ta.trend.MACD(df['close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_histogram'] = macd.macd_diff()

            # Bollinger Bands
            bollinger = ta.volatility.BollingerBands(df['close'])
            df['bb_upper'] = bollinger.bollinger_hband()
            df['bb_middle'] = bollinger.bollinger_mavg()
            df['bb_lower'] = bollinger.bollinger_lband()

            # ATR (Average True Range)
            df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'])

            # Stochastic
            stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'])
            df['stoch_k'] = stoch.stoch()
            df['stoch_d'] = stoch.stoch_signal()

            # Volume indicators
            df['volume_sma'] = ta.volume.volume_sma(df['close'], df['volume'])

        except Exception as e:
            print(f"خطأ في حساب المؤشرات الفنية: {e}")

        return df

    def get_real_time_data(self, symbol: str) -> Dict:
        """الحصول على البيانات الحالية (محاكاة)"""
        try:
            coin_id = self._get_coin_id(symbol)
            if not coin_id:
                raise Exception(f"لم يتم العثور على العملة: {symbol}")

            url = f"{self.base_url}/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true'
            }

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()[coin_id]

            return {
                'symbol': symbol.upper(),
                'price': data['usd'],
                'change_24h': data.get('usd_24h_change', 0),
                'volume_24h': data.get('usd_24h_vol', 0),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"فشل في جلب البيانات الحقيقية، استخدام محاكاة: {e}")
            # بيانات محاكاة
            base_prices = {'BTC': 45000, 'ETH': 3200, 'ADA': 0.52}
            base_price = base_prices.get(symbol.upper(), 100)

            return {
                'symbol': symbol.upper(),
                'price': base_price * (1 + np.random.normal(0, 0.02)),
                'change_24h': np.random.normal(0, 3),
                'volume_24h': np.random.lognormal(20, 1),
                'timestamp': datetime.now().isoformat()
            }