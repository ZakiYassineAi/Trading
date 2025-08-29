import express from 'express';
import { db } from '../models/database.js';
import { authenticateToken } from './auth.js';
import axios from 'axios';

const router = express.Router();

// تشغيل باك-تست
router.post('/run', authenticateToken, async (req, res) => {
  try {
    const { strategyId, symbol, timeframe, startDate, endDate, initialCapital = 10000 } = req.body;

    if (!strategyId || !symbol || !timeframe || !startDate || !endDate) {
      return res.status(400).json({
        error: 'يجب إدخال جميع البيانات المطلوبة'
      });
    }

    // الحصول على الاستراتيجية
    const strategy = await db.get(`
      SELECT * FROM trading_strategies WHERE id = ?
    `, [strategyId]);

    if (!strategy) {
      return res.status(404).json({ error: 'الاستراتيجية غير موجودة' });
    }

    // استدعاء Python engine لتشغيل الباك-تست
    const pythonEngineUrl = process.env.PYTHON_ENGINE_URL || 'http://localhost:5000';

    const backtestData = {
      strategy: {
        type: strategy.type,
        parameters: JSON.parse(strategy.parameters)
      },
      symbol,
      timeframe,
      start_date: startDate,
      end_date: endDate,
      initial_capital: initialCapital
    };

    try {
      // محاولة استدعاء Python engine
      const response = await axios.post(`${pythonEngineUrl}/backtest/run`, backtestData, {
        timeout: 30000 // 30 seconds timeout
      });

      const results = response.data;

      // حفظ نتائج الباك-تست في قاعدة البيانات
      await saveBacktestResults(req.user.userId, strategyId, symbol, timeframe, startDate, endDate, initialCapital, results);

      res.json({
        message: 'تم تشغيل الباك-تست بنجاح',
        results
      });

    } catch (engineError) {
      console.error('Python engine error:', engineError.message);

      // في حالة عدم توفر Python engine، إرجاع نتائج محاكاة للعرض
      const mockResults = generateMockBacktestResults(symbol, timeframe, startDate, endDate, initialCapital, strategy);

      await saveBacktestResults(req.user.userId, strategyId, symbol, timeframe, startDate, endDate, initialCapital, mockResults);

      res.json({
        message: 'تم تشغيل الباك-تست (وضع المحاكاة)',
        results: mockResults,
        note: 'Python engine غير متوفر - تم عرض نتائج محاكاة'
      });
    }
  } catch (error) {
    throw error;
  }
});

// الحصول على نتائج الباك-تست
router.get('/results', authenticateToken, async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;
    const offset = (page - 1) * limit;

    const results = await db.all(`
      SELECT br.*, ts.name as strategy_name, ts.type as strategy_type
      FROM backtest_results br
      LEFT JOIN trading_strategies ts ON br.strategy_id = ts.id
      WHERE br.user_id = ?
      ORDER BY br.created_at DESC
      LIMIT ? OFFSET ?
    `, [req.user.userId, limit, offset]);

    const totalCount = await db.get(`
      SELECT COUNT(*) as count FROM backtest_results WHERE user_id = ?
    `, [req.user.userId]);

    const formattedResults = results.map(result => ({
      ...result,
      metrics: JSON.parse(result.metrics || '{}'),
      equity_curve: JSON.parse(result.equity_curve || '[]'),
      trade_log: JSON.parse(result.trade_log || '[]')
    }));

    res.json({
      results: formattedResults,
      pagination: {
        currentPage: parseInt(page),
        totalPages: Math.ceil(totalCount.count / limit),
        totalCount: totalCount.count,
        limit: parseInt(limit)
      }
    });
  } catch (error) {
    throw error;
  }
});

// حذف نتائج باك-تست
router.delete('/results/:id', authenticateToken, async (req, res) => {
  try {
    const resultId = req.params.id;

    const result = await db.get(`
      SELECT * FROM backtest_results WHERE id = ? AND user_id = ?
    `, [resultId, req.user.userId]);

    if (!result) {
      return res.status(404).json({ error: 'النتيجة غير موجودة' });
    }

    await db.run(`DELETE FROM backtest_results WHERE id = ?`, [resultId]);

    res.json({ message: 'تم حذف نتيجة الباك-تست بنجاح' });
  } catch (error) {
    throw error;
  }
});

// حفظ نتائج الباك-تست
async function saveBacktestResults(userId, strategyId, symbol, timeframe, startDate, endDate, initialCapital, results) {
  await db.run(`
    INSERT INTO backtest_results (
      user_id, strategy_id, symbol, timeframe, start_date, end_date,
      initial_capital, final_capital, total_return, cagr, sharpe_ratio,
      sortino_ratio, max_drawdown, calmar_ratio, hit_rate, total_trades,
      winning_trades, losing_trades, metrics, equity_curve, trade_log
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `, [
    userId, strategyId, symbol, timeframe, startDate, endDate,
    initialCapital, results.final_value, results.total_return, results.cagr,
    results.sharpe_ratio, results.sortino_ratio, results.max_drawdown,
    results.calmar_ratio, results.hit_rate, results.total_trades,
    results.winning_trades, results.losing_trades,
    JSON.stringify(results.metrics || {}),
    JSON.stringify(results.equity_curve || []),
    JSON.stringify(results.trades || [])
  ]);
}

// توليد نتائج محاكاة للباك-تست
function generateMockBacktestResults(symbol, timeframe, startDate, endDate, initialCapital, strategy) {
  // توليد قيم عشوائية واقعية للعرض
  const baseReturn = 0.15 + (Math.random() - 0.5) * 0.3; // عائد من -15% إلى +30%
  const finalValue = initialCapital * (1 + baseReturn);
  const totalTrades = Math.floor(Math.random() * 50) + 10;
  const winRate = 0.4 + Math.random() * 0.3; // معدل نجاح 40-70%
  const winningTrades = Math.floor(totalTrades * winRate);
  const losingTrades = totalTrades - winningTrades;

  // توليد equity curve
  const equityCurve = [];
  let currentValue = initialCapital;
  const days = 100;

  for (let i = 0; i <= days; i++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + i);

    // محاكاة تقلبات واقعية
    if (i > 0) {
      const dailyChange = (Math.random() - 0.5) * 0.05; // تغيير يومي حتى ±2.5%
      currentValue *= (1 + dailyChange);
    }

    equityCurve.push({
      date: date.toISOString().split('T')[0],
      value: Math.round(currentValue * 100) / 100
    });
  }

  // ضبط القيمة النهائية
  equityCurve[equityCurve.length - 1].value = Math.round(finalValue * 100) / 100;

  return {
    initial_value: initialCapital,
    final_value: Math.round(finalValue * 100) / 100,
    total_return: Math.round(baseReturn * 10000) / 100, // نسبة مئوية
    cagr: Math.round(baseReturn * 100 * 100) / 100,
    sharpe_ratio: Math.round((0.5 + Math.random() * 1.5) * 100) / 100,
    sortino_ratio: Math.round((0.6 + Math.random() * 1.8) * 100) / 100,
    max_drawdown: -Math.round((Math.random() * 0.25 + 0.05) * 10000) / 100,
    calmar_ratio: Math.round((0.3 + Math.random() * 1.2) * 100) / 100,
    hit_rate: Math.round(winRate * 10000) / 100,
    total_trades: totalTrades,
    winning_trades: winningTrades,
    losing_trades: losingTrades,
    equity_curve: equityCurve,
    trades: generateMockTrades(totalTrades, winningTrades, symbol),
    metrics: {
      avg_trade_duration: Math.round((Math.random() * 48 + 2) * 100) / 100,
      profit_factor: Math.round((1 + Math.random() * 2) * 100) / 100,
      recovery_factor: Math.round((Math.random() * 3 + 1) * 100) / 100,
      volatility: Math.round((Math.random() * 0.3 + 0.1) * 10000) / 100
    }
  };
}

// توليد صفقات وهمية
function generateMockTrades(totalTrades, winningTrades, symbol) {
  const trades = [];
  const startDate = new Date();
  startDate.setMonth(startDate.getMonth() - 3);

  for (let i = 0; i < totalTrades; i++) {
    const isWinning = i < winningTrades;
    const entryDate = new Date(startDate.getTime() + (i * 24 * 60 * 60 * 1000 * 2));
    const exitDate = new Date(entryDate.getTime() + (Math.random() * 48 * 60 * 60 * 1000));

    const entryPrice = 20000 + Math.random() * 30000;
    const pnlPercent = isWinning ? Math.random() * 0.08 + 0.01 : -Math.random() * 0.05 - 0.005;
    const exitPrice = entryPrice * (1 + pnlPercent);
    const quantity = 0.1 + Math.random() * 0.9;
    const pnl = (exitPrice - entryPrice) * quantity;

    trades.push({
      id: i + 1,
      symbol,
      side: 'buy',
      entry_date: entryDate.toISOString(),
      exit_date: exitDate.toISOString(),
      entry_price: Math.round(entryPrice * 100) / 100,
      exit_price: Math.round(exitPrice * 100) / 100,
      quantity: Math.round(quantity * 10000) / 10000,
      pnl: Math.round(pnl * 100) / 100,
      pnl_percent: Math.round(pnlPercent * 10000) / 100,
      fees: Math.round(entryPrice * quantity * 0.001 * 100) / 100
    });
  }

  return trades;
}

export default router;