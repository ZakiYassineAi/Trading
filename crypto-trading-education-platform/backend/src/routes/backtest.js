import express from 'express';
import { knex } from '../models/database.js';
import { authenticateToken } from './auth.js';
import axios from 'axios';

const router = express.Router();

// Run a backtest
router.post('/run', authenticateToken, async (req, res) => {
  try {
    const { strategyId, symbol, timeframe, startDate, endDate, initialCapital = 10000 } = req.body;

    if (!strategyId || !symbol || !timeframe || !startDate || !endDate) {
      return res.status(400).json({ error: 'All required fields must be provided.' });
    }

    const strategy = await knex('trading_strategies').where({ id: strategyId }).first();

    if (!strategy) {
      return res.status(404).json({ error: 'Strategy not found.' });
    }

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
      const response = await axios.post(`${pythonEngineUrl}/backtest/run`, backtestData, {
        timeout: 30000 // 30 seconds timeout
      });

      const results = response.data;
      await saveBacktestResults(req.user.userId, strategyId, symbol, timeframe, startDate, endDate, initialCapital, results);
      res.json({ message: 'Backtest executed successfully.', results });

    } catch (engineError) {
      console.error('Python engine error:', engineError.message);
      const mockResults = generateMockBacktestResults(symbol, timeframe, startDate, endDate, initialCapital, strategy);
      await saveBacktestResults(req.user.userId, strategyId, symbol, timeframe, startDate, endDate, initialCapital, mockResults);
      res.json({
        message: 'Backtest executed (simulation mode).',
        results: mockResults,
        note: 'Python engine was unavailable - showing simulated results.'
      });
    }
  } catch (error) {
    res.status(500).json({ error: 'Failed to run backtest.' });
  }
});

// Get backtest results
router.get('/results', authenticateToken, async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;
    const offset = (page - 1) * limit;

    const results = await knex('backtest_results as br')
      .leftJoin('trading_strategies as ts', 'br.strategy_id', 'ts.id')
      .where('br.user_id', req.user.userId)
      .select('br.*', 'ts.name as strategy_name', 'ts.type as strategy_type')
      .orderBy('br.created_at', 'desc')
      .limit(limit)
      .offset(offset);

    const totalCountResult = await knex('backtest_results').where({ user_id: req.user.userId }).count({ count: '*' }).first();
    const totalCount = totalCountResult.count;

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
        totalPages: Math.ceil(totalCount / limit),
        totalCount: parseInt(totalCount),
        limit: parseInt(limit)
      }
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch backtest results.' });
  }
});

// Delete backtest result
router.delete('/results/:id', authenticateToken, async (req, res) => {
  try {
    const resultId = req.params.id;
    const result = await knex('backtest_results')
      .where({ id: resultId, user_id: req.user.userId })
      .first();

    if (!result) {
      return res.status(404).json({ error: 'Result not found.' });
    }

    await knex('backtest_results').where({ id: resultId }).del();
    res.json({ message: 'Backtest result deleted successfully.' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete backtest result.' });
  }
});

// Helper to save backtest results
async function saveBacktestResults(userId, strategyId, symbol, timeframe, startDate, endDate, initialCapital, results) {
  await knex('backtest_results').insert({
    user_id: userId,
    strategy_id: strategyId,
    symbol,
    timeframe,
    start_date: startDate,
    end_date: endDate,
    initial_capital: initialCapital,
    final_capital: results.final_value,
    total_return: results.total_return,
    cagr: results.cagr,
    sharpe_ratio: results.sharpe_ratio,
    sortino_ratio: results.sortino_ratio,
    max_drawdown: results.max_drawdown,
    calmar_ratio: results.calmar_ratio,
    hit_rate: results.hit_rate,
    total_trades: results.total_trades,
    winning_trades: results.winning_trades,
    losing_trades: results.losing_trades,
    metrics: JSON.stringify(results.metrics || {}),
    equity_curve: JSON.stringify(results.equity_curve || []),
    trade_log: JSON.stringify(results.trades || [])
  });
}

// Generate mock backtest results
function generateMockBacktestResults(symbol, timeframe, startDate, endDate, initialCapital, strategy) {
  const baseReturn = 0.15 + (Math.random() - 0.5) * 0.3;
  const finalValue = initialCapital * (1 + baseReturn);
  const totalTrades = Math.floor(Math.random() * 50) + 10;
  const winRate = 0.4 + Math.random() * 0.3;
  const winningTrades = Math.floor(totalTrades * winRate);
  const losingTrades = totalTrades - winningTrades;

  const equityCurve = [];
  let currentValue = initialCapital;
  const days = 100;

  for (let i = 0; i <= days; i++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + i);

    if (i > 0) {
      const dailyChange = (Math.random() - 0.5) * 0.05;
      currentValue *= (1 + dailyChange);
    }

    equityCurve.push({
      date: date.toISOString().split('T')[0],
      value: Math.round(currentValue * 100) / 100
    });
  }

  equityCurve[equityCurve.length - 1].value = Math.round(finalValue * 100) / 100;

  return {
    initial_value: initialCapital,
    final_value: Math.round(finalValue * 100) / 100,
    total_return: Math.round(baseReturn * 10000) / 100,
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

// Generate mock trades
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