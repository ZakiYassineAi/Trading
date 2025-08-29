import express from 'express';
import { db } from '../models/database.js';
import { authenticateToken } from './auth.js';

const router = express.Router();

// الحصول على جميع المحافظ للمستخدم
router.get('/', authenticateToken, async (req, res) => {
  try {
    const portfolios = await db.all(`
      SELECT * FROM paper_portfolios WHERE user_id = ?
      ORDER BY created_at DESC
    `, [req.user.userId]);

    // حساب إجمالي الأداء لكل محفظة
    for (const portfolio of portfolios) {
      const trades = await db.all(`
        SELECT * FROM paper_trades WHERE portfolio_id = ?
        ORDER BY executed_at DESC
      `, [portfolio.id]);

      portfolio.trades = trades;
      portfolio.total_trades = trades.length;
      portfolio.total_profit_loss = trades.reduce((sum, trade) => {
        const pnl = trade.side === 'sell' ?
          (trade.price * trade.quantity - trade.total_amount) :
          -(trade.price * trade.quantity + trade.fees);
        return sum + pnl;
      }, 0);
      portfolio.return_percentage = portfolio.initial_balance > 0 ?
        ((portfolio.current_balance - portfolio.initial_balance) / portfolio.initial_balance * 100) : 0;
    }

    res.json({ portfolios });
  } catch (error) {
    throw error;
  }
});

// إنشاء محفظة جديدة
router.post('/', authenticateToken, async (req, res) => {
  try {
    const { name, initialBalance = 10000, currency = 'USD' } = req.body;

    if (!name) {
      return res.status(400).json({ error: 'يجب إدخال اسم المحفظة' });
    }

    if (initialBalance < 1000 || initialBalance > 1000000) {
      return res.status(400).json({
        error: 'الرصيد الابتدائي يجب أن يكون بين 1,000 و 1,000,000'
      });
    }

    const result = await db.run(`
      INSERT INTO paper_portfolios (user_id, name, initial_balance, current_balance, currency)
      VALUES (?, ?, ?, ?, ?)
    `, [req.user.userId, name, initialBalance, initialBalance, currency]);

    const portfolio = await db.get(`
      SELECT * FROM paper_portfolios WHERE id = ?
    `, [result.lastID]);

    res.status(201).json({
      message: 'تم إنشاء المحفظة بنجاح',
      portfolio
    });
  } catch (error) {
    throw error;
  }
});

// تنفيذ صفقة وهمية (شراء/بيع)
router.post('/:id/trade', authenticateToken, async (req, res) => {
  try {
    const portfolioId = req.params.id;
    const { symbol, side, quantity, price, strategySignal, notes } = req.body;

    if (!symbol || !side || !quantity || !price) {
      return res.status(400).json({
        error: 'يجب إدخال جميع بيانات الصفقة'
      });
    }

    if (!['buy', 'sell'].includes(side)) {
      return res.status(400).json({ error: 'نوع الصفقة يجب أن يكون buy أو sell' });
    }

    // التحقق من ملكية المحفظة
    const portfolio = await db.get(`
      SELECT * FROM paper_portfolios WHERE id = ? AND user_id = ? AND status = 'active'
    `, [portfolioId, req.user.userId]);

    if (!portfolio) {
      return res.status(404).json({
        error: 'المحفظة غير موجودة أو غير نشطة'
      });
    }

    // حساب إجمالي الصفقة والرسوم
    const totalAmount = quantity * price;
    const fees = totalAmount * 0.001; // 0.1% رسوم
    const totalCost = totalAmount + fees;

    // التحقق من توفر الرصيد للشراء
    if (side === 'buy' && portfolio.current_balance < totalCost) {
      return res.status(400).json({
        error: 'رصيد غير كافي لإتمام الصفقة'
      });
    }

    // تنفيذ الصفقة الوهمية
    await db.run(`
      INSERT INTO paper_trades (
        portfolio_id, symbol, side, quantity, price, total_amount, fees,
        strategy_signal, notes
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `, [portfolioId, symbol.toUpperCase(), side, quantity, price, totalAmount, fees, strategySignal, notes]);

    // تحديث رصيد المحفظة
    const newBalance = side === 'buy' ?
      portfolio.current_balance - totalCost :
      portfolio.current_balance + (totalAmount - fees);

    await db.run(`
      UPDATE paper_portfolios SET current_balance = ?, updated_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `, [newBalance, portfolioId]);

    res.json({
      message: `تم تنفيذ صفقة ${side === 'buy' ? 'شراء' : 'بيع'} بنجاح`,
      trade: {
        symbol: symbol.toUpperCase(),
        side,
        quantity,
        price,
        total_amount: totalAmount,
        fees,
        new_balance: newBalance
      },
      paperTradingOnly: true
    });
  } catch (error) {
    throw error;
  }
});

// الحصول على تاريخ الصفقات لمحفظة
router.get('/:id/trades', authenticateToken, async (req, res) => {
  try {
    const portfolioId = req.params.id;
    const { page = 1, limit = 20 } = req.query;
    const offset = (page - 1) * limit;

    // التحقق من ملكية المحفظة
    const portfolio = await db.get(`
      SELECT * FROM paper_portfolios WHERE id = ? AND user_id = ?
    `, [portfolioId, req.user.userId]);

    if (!portfolio) {
      return res.status(404).json({ error: 'المحفظة غير موجودة' });
    }

    const trades = await db.all(`
      SELECT * FROM paper_trades WHERE portfolio_id = ?
      ORDER BY executed_at DESC
      LIMIT ? OFFSET ?
    `, [portfolioId, limit, offset]);

    const totalCount = await db.get(`
      SELECT COUNT(*) as count FROM paper_trades WHERE portfolio_id = ?
    `, [portfolioId]);

    res.json({
      trades,
      portfolio: {
        name: portfolio.name,
        current_balance: portfolio.current_balance,
        initial_balance: portfolio.initial_balance
      },
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

// حذف محفظة
router.delete('/:id', authenticateToken, async (req, res) => {
  try {
    const portfolioId = req.params.id;

    const portfolio = await db.get(`
      SELECT * FROM paper_portfolios WHERE id = ? AND user_id = ?
    `, [portfolioId, req.user.userId]);

    if (!portfolio) {
      return res.status(404).json({ error: 'المحفظة غير موجودة' });
    }

    // حذف جميع الصفقات المرتبطة
    await db.run(`DELETE FROM paper_trades WHERE portfolio_id = ?`, [portfolioId]);

    // حذف المحفظة
    await db.run(`DELETE FROM paper_portfolios WHERE id = ?`, [portfolioId]);

    res.json({ message: 'تم حذف المحفظة وجميع صفقاتها بنجاح' });
  } catch (error) {
    throw error;
  }
});

// إعادة تعيين محفظة (إعادة الرصيد إلى القيمة الابتدائية)
router.post('/:id/reset', authenticateToken, async (req, res) => {
  try {
    const portfolioId = req.params.id;

    const portfolio = await db.get(`
      SELECT * FROM paper_portfolios WHERE id = ? AND user_id = ?
    `, [portfolioId, req.user.userId]);

    if (!portfolio) {
      return res.status(404).json({ error: 'المحفظة غير موجودة' });
    }

    // حذف جميع الصفقات
    await db.run(`DELETE FROM paper_trades WHERE portfolio_id = ?`, [portfolioId]);

    // إعادة تعيين الرصيد
    await db.run(`
      UPDATE paper_portfolios
      SET current_balance = initial_balance, updated_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `, [portfolioId]);

    res.json({
      message: 'تم إعادة تعيين المحفظة بنجاح',
      balance: portfolio.initial_balance
    });
  } catch (error) {
    throw error;
  }
});

export default router;