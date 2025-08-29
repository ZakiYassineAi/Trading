import express from 'express';
import { db } from '../models/database.js';
import { authenticateToken } from './auth.js';

const router = express.Router();

// الحصول على جميع الاستراتيجيات
router.get('/', authenticateToken, async (req, res) => {
  try {
    const strategies = await db.all(`
      SELECT * FROM trading_strategies
      WHERE user_id = ? OR user_id IS NULL
      ORDER BY created_at DESC
    `, [req.user.userId]);

    const formattedStrategies = strategies.map(strategy => ({
      ...strategy,
      parameters: JSON.parse(strategy.parameters || '{}')
    }));

    res.json({ strategies: formattedStrategies });
  } catch (error) {
    throw error;
  }
});

// إنشاء استراتيجية جديدة
router.post('/', authenticateToken, async (req, res) => {
  try {
    const { name, type, parameters, description } = req.body;

    if (!name || !type || !parameters) {
      return res.status(400).json({
        error: 'يجب إدخال اسم ونوع ومعاملات الاستراتيجية'
      });
    }

    // التحقق من أن نوع الاستراتيجية معتمد
    const validTypes = ['SMA', 'EMA', 'RSI', 'MACD', 'BREAKOUT', 'ATR', 'MEAN_REVERSION', 'VOLATILITY_TARGETING'];
    if (!validTypes.includes(type)) {
      return res.status(400).json({
        error: 'نوع الاستراتيجية غير معتمد'
      });
    }

    const result = await db.run(`
      INSERT INTO trading_strategies (user_id, name, type, parameters, description)
      VALUES (?, ?, ?, ?, ?)
    `, [req.user.userId, name, type, JSON.stringify(parameters), description]);

    const strategy = await db.get(`
      SELECT * FROM trading_strategies WHERE id = ?
    `, [result.lastID]);

    res.status(201).json({
      message: 'تم إنشاء الاستراتيجية بنجاح',
      strategy: {
        ...strategy,
        parameters: JSON.parse(strategy.parameters)
      }
    });
  } catch (error) {
    throw error;
  }
});

// تحديث استراتيجية
router.put('/:id', authenticateToken, async (req, res) => {
  try {
    const { name, parameters, description, isActive } = req.body;
    const strategyId = req.params.id;

    // التحقق من ملكية الاستراتيجية
    const strategy = await db.get(`
      SELECT * FROM trading_strategies WHERE id = ? AND user_id = ?
    `, [strategyId, req.user.userId]);

    if (!strategy) {
      return res.status(404).json({
        error: 'الاستراتيجية غير موجودة أو لا تملك صلاحية الوصول'
      });
    }

    await db.run(`
      UPDATE trading_strategies
      SET name = ?, parameters = ?, description = ?, is_active = ?, updated_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `, [name || strategy.name,
        JSON.stringify(parameters || JSON.parse(strategy.parameters)),
        description || strategy.description,
        isActive !== undefined ? isActive : strategy.is_active,
        strategyId]);

    const updatedStrategy = await db.get(`
      SELECT * FROM trading_strategies WHERE id = ?
    `, [strategyId]);

    res.json({
      message: 'تم تحديث الاستراتيجية بنجاح',
      strategy: {
        ...updatedStrategy,
        parameters: JSON.parse(updatedStrategy.parameters)
      }
    });
  } catch (error) {
    throw error;
  }
});

// حذف استراتيجية
router.delete('/:id', authenticateToken, async (req, res) => {
  try {
    const strategyId = req.params.id;

    // التحقق من ملكية الاستراتيجية
    const strategy = await db.get(`
      SELECT * FROM trading_strategies WHERE id = ? AND user_id = ?
    `, [strategyId, req.user.userId]);

    if (!strategy) {
      return res.status(404).json({
        error: 'الاستراتيجية غير موجودة أو لا تملك صلاحية الوصول'
      });
    }

    await db.run(`DELETE FROM trading_strategies WHERE id = ?`, [strategyId]);

    res.json({ message: 'تم حذف الاستراتيجية بنجاح' });
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