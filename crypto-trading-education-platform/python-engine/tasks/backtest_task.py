import os
import json
import hashlib
from redis import Redis
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

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

# Cache expiration time in seconds (e.g., 24 hours)
CACHE_EXPIRATION = 24 * 60 * 60

@celery.task
def run_backtest_task(strategy_config, symbol, timeframe, start_date, end_date, initial_capital):
    """Celery task to run a backtest for a given strategy, with caching."""
    # Create a stable cache key
    params = {
        'strategy': strategy_config,
        'symbol': symbol,
        'timeframe': timeframe,
        'start': start_date,
        'end': end_date,
        'capital': initial_capital
    }
    params_str = json.dumps(params, sort_keys=True)
    cache_key = f"backtest:{hashlib.md5(params_str.encode()).hexdigest()}"

    # Try to get the result from cache
    try:
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)
    except Exception as e:
        # If Redis fails, just log and continue without caching
        print(f"Redis cache read failed: {e}")


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

    # Store the result in cache
    try:
        # We need a custom JSON encoder for pandas Timestamps if they exist
        result_str = json.dumps(final_results, default=str)
        redis_client.set(cache_key, result_str, ex=CACHE_EXPIRATION)
    except Exception as e:
        print(f"Redis cache write failed: {e}")

    return final_results
