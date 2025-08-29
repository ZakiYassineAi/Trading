from celery_app import celery
from strategies.sma_strategy import SMAStrategy
from strategies.ema_strategy import EMAStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy
from strategies.breakout_strategy import BreakoutStrategy
from strategies.atr_strategy import ATRStrategy
from strategies.mean_reversion_strategy import MeanReversionStrategy
from strategies.volatility_targeting_strategy import VolatilityTargetingStrategy
from backtesting.backtest_engine import BacktestEngine
from data.data_provider import DataProvider
from utils.performance_metrics import PerformanceMetrics

# Dictionary of available strategies
STRATEGIES = {
    'SMA': SMAStrategy,
    'EMA': EMAStrategy,
    'RSI': RSIStrategy,
    'MACD': MACDStrategy,
    'BREAKOUT': BreakoutStrategy,
    'ATR': ATRStrategy,
    'MEAN_REVERSION': MeanReversionStrategy,
    'VOLATILITY_TARGETING': VolatilityTargetingStrategy
}

@celery.task
def run_backtest_task(strategy_config, symbol, timeframe, start_date, end_date, initial_capital):
    """Celery task to run a backtest for a given strategy."""
    strategy_type = strategy_config['type']
    strategy_params = strategy_config['parameters']

    if strategy_type not in STRATEGIES:
        raise ValueError(f'Strategy type {strategy_type} not supported')

    data_provider = DataProvider()
    market_data = data_provider.get_data(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        timeframe=timeframe
    )

    if market_data.empty:
        raise ValueError('No data available for the given period')

    strategy_class = STRATEGIES[strategy_type]
    strategy = strategy_class(**strategy_params)

    engine = BacktestEngine(
        initial_capital=initial_capital,
        commission=0.001,
        slippage=0.0001
    )

    results = engine.run(strategy, market_data)

    metrics = PerformanceMetrics()
    performance_stats = metrics.calculate_all_metrics(
        results['equity_curve'],
        results['trades'],
        initial_capital
    )

    final_results = {
        'initial_value': initial_capital,
        'final_value': results['final_capital'],
        'total_return': performance_stats['total_return'],
        'cagr': performance_stats['cagr'],
        'sharpe_ratio': performance_stats['sharpe_ratio'],
        'sortino_ratio': performance_stats['sortino_ratio'],
        'max_drawdown': performance_stats['max_drawdown'],
        'calmar_ratio': performance_stats['calmar_ratio'],
        'hit_rate': performance_stats['hit_rate'],
        'total_trades': len(results['trades']),
        'winning_trades': performance_stats['winning_trades'],
        'losing_trades': performance_stats['losing_trades'],
        'equity_curve': results['equity_curve'].to_dict('records'),
        'trades': results['trades'],
        'metrics': performance_stats,
        'strategy_info': {
            'type': strategy_type,
            'parameters': strategy_params
        }
    }

    return final_results
