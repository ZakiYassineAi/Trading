from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import os
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

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])

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

@app.route('/health', methods=['GET'])
def health_check():
    """فحص حالة محرك Python"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'available_strategies': list(STRATEGIES.keys()),
        'message': 'محرك Python للباك-تست جاهز'
    })

@app.route('/backtest/run', methods=['POST'])
def run_backtest():
    """تشغيل باك-تست لاستراتيجية معينة"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        required_fields = ['strategy', 'symbol', 'timeframe', 'start_date', 'end_date', 'initial_capital']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'حقل {field} مطلوب'}), 400

        strategy_config = data['strategy']
        strategy_type = strategy_config['type']
        strategy_params = strategy_config['parameters']

        if strategy_type not in STRATEGIES:
            return jsonify({'error': f'نوع الاستراتيجية {strategy_type} غير مدعوم'}), 400

        # الحصول على البيانات
        data_provider = DataProvider()
        market_data = data_provider.get_data(
            symbol=data['symbol'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            timeframe=data['timeframe']
        )

        if market_data.empty:
            return jsonify({'error': 'لا توجد بيانات متاحة للفترة المحددة'}), 400

        # إنشاء الاستراتيجية
        strategy_class = STRATEGIES[strategy_type]
        strategy = strategy_class(**strategy_params)

        # إنشاء محرك الباك-تست
        engine = BacktestEngine(
            initial_capital=data['initial_capital'],
            commission=0.001,  # 0.1% رسوم
            slippage=0.0001   # 0.01% انزلاق
        )

        # تشغيل الباك-تست
        results = engine.run(strategy, market_data)

        # حساب المقاييس المتقدمة
        metrics = PerformanceMetrics()
        performance_stats = metrics.calculate_all_metrics(
            results['equity_curve'],
            results['trades'],
            data['initial_capital']
        )

        # تجهيز النتائج النهائية
        final_results = {
            'initial_value': data['initial_capital'],
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

        return jsonify(final_results)

    except Exception as e:
        print(f"خطأ في الباك-تست: {str(e)}")
        return jsonify({'error': f'حدث خطأ في تشغيل الباك-تست: {str(e)}'}), 500

@app.route('/strategies/list', methods=['GET'])
def list_strategies():
    """الحصول على قائمة الاستراتيجيات المتاحة"""
    strategies_info = {}

    for name, strategy_class in STRATEGIES.items():
        strategies_info[name] = {
            'name': name,
            'description': getattr(strategy_class, 'description', 'لا يوجد وصف'),
            'parameters': getattr(strategy_class, 'default_parameters', {})
        }

    return jsonify({
        'strategies': strategies_info,
        'count': len(strategies_info)
    })

@app.route('/data/indicators/<symbol>', methods=['GET'])
def get_technical_indicators(symbol):
    """حساب المؤشرات الفنية لرمز معين"""
    try:
        start_date = request.args.get('start_date', '2023-01-01')
        end_date = request.args.get('end_date', '2024-01-01')
        timeframe = request.args.get('timeframe', '1d')

        data_provider = DataProvider()
        market_data = data_provider.get_data(symbol, start_date, end_date, timeframe)

        if market_data.empty:
            return jsonify({'error': 'لا توجد بيانات متاحة'}), 404

        # حساب المؤشرات الفنية
        indicators = data_provider.calculate_technical_indicators(market_data)

        return jsonify({
            'symbol': symbol,
            'timeframe': timeframe,
            'indicators': indicators.to_dict('records'),
            'period': {
                'start': start_date,
                'end': end_date
            }
        })

    except Exception as e:
        return jsonify({'error': f'خطأ في حساب المؤشرات: {str(e)}'}), 500

@app.route('/optimize/grid-search', methods=['POST'])
def grid_search_optimization():
    """تحسين معاملات الاستراتيجية باستخدام Grid Search"""
    try:
        data = request.get_json()

        # TODO: تنفيذ Grid Search للتحسين
        # هذا يتطلب وقت أكثر للتطوير الكامل

        return jsonify({
            'message': 'Grid Search قيد التطوير',
            'status': 'coming_soon'
        })

    except Exception as e:
        return jsonify({'error': f'خطأ في التحسين: {str(e)}'}), 500

if __name__ == '__main__':
    print("🐍 بدء تشغيل محرك Python للباك-تست...")
    print(f"🔧 الاستراتيجيات المتاحة: {list(STRATEGIES.keys())}")
    print("🌐 المحرك متاح على: http://localhost:5000")
    print("🛡️  وضع Paper Trading فقط - آمن تماماً")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )