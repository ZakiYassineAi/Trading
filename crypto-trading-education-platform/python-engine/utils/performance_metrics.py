import pandas as pd
import numpy as np
from typing import Dict, List
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class PerformanceMetrics:
    """حاسبة مقاييس الأداء المتقدمة لاستراتيجيات التداول"""

    def __init__(self, risk_free_rate: float = 0.02):
        """
        :param risk_free_rate: معدل العائد الخالي من المخاطر (افتراضي 2%)
        """
        self.risk_free_rate = risk_free_rate

    def calculate_all_metrics(self, equity_curve: pd.DataFrame, trades: List[Dict], initial_capital: float) -> Dict:
        """حساب جميع مقاييس الأداء المتقدمة"""
        if equity_curve.empty:
            return self._get_empty_metrics()

        try:
            # استخراج قيم المحفظة
            portfolio_values = equity_curve['portfolio_value'].values

            # حساب العوائد اليومية
            returns = self._calculate_returns(portfolio_values)

            # المقاييس الأساسية
            total_return = self._calculate_total_return(portfolio_values[0], portfolio_values[-1])
            cagr = self._calculate_cagr(portfolio_values[0], portfolio_values[-1], len(portfolio_values))

            # مقاييس المخاطر
            max_drawdown = self._calculate_max_drawdown(portfolio_values)
            volatility = self._calculate_volatility(returns)

            # مقاييس معدلة بالمخاطر
            sharpe_ratio = self._calculate_sharpe_ratio(returns)
            sortino_ratio = self._calculate_sortino_ratio(returns)
            calmar_ratio = self._calculate_calmar_ratio(cagr, max_drawdown)

            # مقاييس الصفقات
            trade_metrics = self._calculate_trade_metrics(trades)

            # مقاييس إضافية
            var_95 = self._calculate_var(returns, 0.05)
            recovery_factor = self._calculate_recovery_factor(total_return, max_drawdown)
            profit_factor = self._calculate_profit_factor(trades)

            return {
                # العوائد والنمو
                'total_return': round(total_return, 2),
                'cagr': round(cagr, 2),
                'annualized_volatility': round(volatility * np.sqrt(252) * 100, 2),

                # مقاييس معدلة بالمخاطر
                'sharpe_ratio': round(sharpe_ratio, 3),
                'sortino_ratio': round(sortino_ratio, 3),
                'calmar_ratio': round(calmar_ratio, 3),

                # مقاييس الهبوط
                'max_drawdown': round(max_drawdown, 2),
                'avg_drawdown': round(np.mean(equity_curve['drawdown']), 2),
                'recovery_factor': round(recovery_factor, 3),

                # مقاييس الصفقات
                'total_trades': trade_metrics['total_trades'],
                'winning_trades': trade_metrics['winning_trades'],
                'losing_trades': trade_metrics['losing_trades'],
                'hit_rate': round(trade_metrics['hit_rate'], 2),
                'profit_factor': round(profit_factor, 3),

                # مقاييس إضافية
                'var_95': round(var_95 * 100, 2),  # Value at Risk 95%
                'skewness': round(stats.skew(returns), 3),
                'kurtosis': round(stats.kurtosis(returns), 3),
                'best_trade': round(max([t['pnl_percent'] for t in trades], default=0), 2),
                'worst_trade': round(min([t['pnl_percent'] for t in trades], default=0), 2),
                'avg_trade_duration': trade_metrics['avg_duration'],

                # معلومات عامة
                'start_date': str(equity_curve['timestamp'].iloc[0]),
                'end_date': str(equity_curve['timestamp'].iloc[-1]),
                'total_days': len(equity_curve)
            }

        except Exception as e:
            print(f"خطأ في حساب مقاييس الأداء: {e}")
            return self._get_empty_metrics()

    def _calculate_returns(self, portfolio_values: np.ndarray) -> np.ndarray:
        """حساب العوائد اليومية"""
        if len(portfolio_values) < 2:
            return np.array([0])

        returns = np.diff(portfolio_values) / portfolio_values[:-1]
        return returns[np.isfinite(returns)]  # إزالة القيم غير المحدودة

    def _calculate_total_return(self, initial_value: float, final_value: float) -> float:
        """حساب إجمالي العائد"""
        if initial_value <= 0:
            return 0
        return ((final_value - initial_value) / initial_value) * 100

    def _calculate_cagr(self, initial_value: float, final_value: float, periods: int) -> float:
        """حساب معدل النمو السنوي المركب (CAGR)"""
        if initial_value <= 0 or final_value <= 0 or periods <= 0:
            return 0

        years = periods / 252  # افتراض 252 يوم تداول في السنة
        if years <= 0:
            return 0

        return (((final_value / initial_value) ** (1 / years)) - 1) * 100

    def _calculate_max_drawdown(self, portfolio_values: np.ndarray) -> float:
        """حساب أقصى هبوط"""
        if len(portfolio_values) == 0:
            return 0

        peak = portfolio_values[0]
        max_dd = 0

        for value in portfolio_values:
            if value > peak:
                peak = value

            drawdown = (peak - value) / peak * 100
            if drawdown > max_dd:
                max_dd = drawdown

        return max_dd

    def _calculate_volatility(self, returns: np.ndarray) -> float:
        """حساب التقلبات (الانحراف المعياري للعوائد)"""
        if len(returns) == 0:
            return 0
        return np.std(returns, ddof=1)

    def _calculate_sharpe_ratio(self, returns: np.ndarray) -> float:
        """حساب نسبة Sharpe"""
        if len(returns) == 0:
            return 0

        excess_returns = returns - (self.risk_free_rate / 252)  # تحويل إلى عائد يومي

        if np.std(excess_returns, ddof=1) == 0:
            return 0

        return (np.mean(excess_returns) / np.std(excess_returns, ddof=1)) * np.sqrt(252)

    def _calculate_sortino_ratio(self, returns: np.ndarray) -> float:
        """حساب نسبة Sortino (معدلة بالتقلبات الهبوطية فقط)"""
        if len(returns) == 0:
            return 0

        excess_returns = returns - (self.risk_free_rate / 252)
        downside_returns = excess_returns[excess_returns < 0]

        if len(downside_returns) == 0 or np.std(downside_returns, ddof=1) == 0:
            return np.inf if np.mean(excess_returns) > 0 else 0

        return (np.mean(excess_returns) / np.std(downside_returns, ddof=1)) * np.sqrt(252)

    def _calculate_calmar_ratio(self, cagr: float, max_drawdown: float) -> float:
        """حساب نسبة Calmar (CAGR / Max Drawdown)"""
        if max_drawdown == 0:
            return np.inf if cagr > 0 else 0
        return (cagr / 100) / (max_drawdown / 100)

    def _calculate_trade_metrics(self, trades: List[Dict]) -> Dict:
        """حساب مقاييس الصفقات"""
        if not trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'hit_rate': 0,
                'avg_duration': 0
            }

        winning_trades = len([t for t in trades if t['pnl'] > 0])
        losing_trades = len([t for t in trades if t['pnl'] < 0])
        total_trades = len(trades)

        hit_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0

        # حساب متوسط مدة الصفقة
        avg_duration = np.mean([t.get('duration_bars', 1) for t in trades]) if trades else 0

        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'hit_rate': hit_rate,
            'avg_duration': avg_duration
        }

    def _calculate_var(self, returns: np.ndarray, confidence_level: float) -> float:
        """حساب Value at Risk"""
        if len(returns) == 0:
            return 0
        return np.percentile(returns, confidence_level * 100)

    def _calculate_recovery_factor(self, total_return: float, max_drawdown: float) -> float:
        """حساب عامل الاسترداد (Total Return / Max Drawdown)"""
        if max_drawdown == 0:
            return np.inf if total_return > 0 else 0
        return total_return / max_drawdown

    def _calculate_profit_factor(self, trades: List[Dict]) -> float:
        """حساب عامل الربح (Gross Profit / Gross Loss)"""
        if not trades:
            return 0

        gross_profit = sum([t['pnl'] for t in trades if t['pnl'] > 0])
        gross_loss = abs(sum([t['pnl'] for t in trades if t['pnl'] < 0]))

        if gross_loss == 0:
            return np.inf if gross_profit > 0 else 0

        return gross_profit / gross_loss

    def _get_empty_metrics(self) -> Dict:
        """إرجاع مقاييس فارغة في حالة عدم وجود بيانات"""
        return {
            'total_return': 0,
            'cagr': 0,
            'annualized_volatility': 0,
            'sharpe_ratio': 0,
            'sortino_ratio': 0,
            'calmar_ratio': 0,
            'max_drawdown': 0,
            'avg_drawdown': 0,
            'recovery_factor': 0,
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'hit_rate': 0,
            'profit_factor': 0,
            'var_95': 0,
            'skewness': 0,
            'kurtosis': 0,
            'best_trade': 0,
            'worst_trade': 0,
            'avg_trade_duration': 0,
            'start_date': '',
            'end_date': '',
            'total_days': 0
        }