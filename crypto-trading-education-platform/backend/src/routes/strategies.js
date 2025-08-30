import express from 'express';
import { knex } from '../models/database.js';
import { authenticateToken } from './auth.js';

const router = express.Router();

// Get all strategies
router.get('/', authenticateToken, async (req, res) => {
  try {
    const strategies = await knex('trading_strategies')
      .where('user_id', req.user.userId)
      .orWhereNull('user_id')
      .orderBy('created_at', 'desc');

    const formattedStrategies = strategies.map(strategy => ({
      ...strategy,
      parameters: JSON.parse(strategy.parameters || '{}')
    }));

    res.json({ strategies: formattedStrategies });
  } catch (error) {
    throw error;
  }
});

// Create a new strategy
router.post('/', authenticateToken, async (req, res) => {
  try {
    const { name, type, parameters, description } = req.body;

    if (!name || !type || !parameters) {
      return res.status(400).json({
        error: 'Name, type, and parameters are required for the strategy.'
      });
    }

    // Validate strategy type
    const validTypes = ['SMA', 'EMA', 'RSI', 'MACD', 'BREAKOUT', 'ATR', 'MEAN_REVERSION', 'VOLATILITY_TARGETING'];
    if (!validTypes.includes(type)) {
      return res.status(400).json({
        error: 'Unsupported strategy type.'
      });
    }

    const [newStrategyId] = await knex('trading_strategies').insert({
      user_id: req.user.userId,
      name,
      type,
      parameters: JSON.stringify(parameters),
      description
    }).returning('id');

    const strategy = await knex('trading_strategies').where({ id: newStrategyId }).first();

    res.status(201).json({
      message: 'Strategy created successfully.',
      strategy: {
        ...strategy,
        parameters: JSON.parse(strategy.parameters)
      }
    });
  } catch (error) {
    throw error;
  }
});

// Update a strategy
router.put('/:id', authenticateToken, async (req, res) => {
  try {
    const { name, parameters, description, isActive } = req.body;
    const strategyId = req.params.id;

    // Verify ownership
    const strategy = await knex('trading_strategies')
      .where({ id: strategyId, user_id: req.user.userId })
      .first();

    if (!strategy) {
      return res.status(404).json({
        error: 'Strategy not found or you do not have access.'
      });
    }

    await knex('trading_strategies')
      .where({ id: strategyId })
      .update({
        name: name || strategy.name,
        parameters: JSON.stringify(parameters || JSON.parse(strategy.parameters)),
        description: description || strategy.description,
        is_active: isActive !== undefined ? isActive : strategy.is_active,
        updated_at: knex.fn.now()
      });

    const updatedStrategy = await knex('trading_strategies').where({ id: strategyId }).first();

    res.json({
      message: 'Strategy updated successfully.',
      strategy: {
        ...updatedStrategy,
        parameters: JSON.parse(updatedStrategy.parameters)
      }
    });
  } catch (error) {
    throw error;
  }
});

// Delete a strategy
router.delete('/:id', authenticateToken, async (req, res) => {
  try {
    const strategyId = req.params.id;

    // Verify ownership
    const strategy = await knex('trading_strategies')
      .where({ id: strategyId, user_id: req.user.userId })
      .first();

    if (!strategy) {
      return res.status(404).json({
        error: 'Strategy not found or you do not have access.'
      });
    }

    await knex('trading_strategies').where({ id: strategyId }).del();

    res.json({ message: 'Strategy deleted successfully.' });
  } catch (error) {
    throw error;
  }
});

// قوالب الاستراتيجيات الجاهزة
router.get('/templates', (req, res) => {
  const templates = [
    {
      type: 'SMA',
      name: 'استراتيجية تقاطع المتوسط المتحرك البسيط',
      parameters: { fast: 10, slow: 30, symbol: 'BTC' },
      description: 'شراء عند تقاطع المتوسط السريع فوق البطيء'
    },
    {
      type: 'EMA',
      name: 'استراتيجية تقاطع المتوسط المتحرك الأسي',
      parameters: { fast: 12, slow: 26, symbol: 'ETH' },
      description: 'استراتيجية مع استجابة أسرع للتغيرات'
    },
    {
      type: 'RSI',
      name: 'استراتيجية مؤشر القوة النسبية',
      parameters: { period: 14, oversold: 30, overbought: 70, symbol: 'BTC' },
      description: 'شراء عند انخفاض المؤشر وبيع عند ارتفاعه'
    },
    {
      type: 'MACD',
      name: 'استراتيجية MACD',
      parameters: { fast: 12, slow: 26, signal: 9, symbol: 'ETH' },
      description: 'استراتيجية متقدمة للزخم والاتجاه'
    }
  ];

  res.json({ templates });
});

export default router;