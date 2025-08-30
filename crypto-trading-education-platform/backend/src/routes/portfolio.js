import express from 'express';
import { knex } from '../models/database.js';
import { authenticateToken } from './auth.js';

const router = express.Router();

// Get all portfolios for a user
router.get('/', authenticateToken, async (req, res) => {
  try {
    const portfolios = await knex('paper_portfolios')
      .where({ user_id: req.user.userId })
      .orderBy('created_at', 'desc');

    for (const portfolio of portfolios) {
      const trades = await knex('paper_trades')
        .where({ portfolio_id: portfolio.id })
        .orderBy('executed_at', 'desc');

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
    console.error(error);
    res.status(500).json({ error: 'Failed to fetch portfolios.' });
  }
});

// Create a new portfolio
router.post('/', authenticateToken, async (req, res) => {
  try {
    const { name, initialBalance = 10000, currency = 'USD' } = req.body;

    if (!name) {
      return res.status(400).json({ error: 'Portfolio name is required.' });
    }

    if (initialBalance < 1000 || initialBalance > 1000000) {
      return res.status(400).json({ error: 'Initial balance must be between 1,000 and 1,000,000.' });
    }

    const [newPortfolioIdObj] = await knex('paper_portfolios').insert({
      user_id: req.user.userId,
      name,
      initial_balance: initialBalance,
      current_balance: initialBalance,
      currency
    }).returning('id');

    const newPortfolioId = (newPortfolioIdObj.id || newPortfolioIdObj);

    const portfolio = await knex('paper_portfolios').where({ id: newPortfolioId }).first();

    res.status(201).json({
      message: 'Portfolio created successfully.',
      portfolio
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to create portfolio.' });
  }
});

// Execute a paper trade
router.post('/:id/trade', authenticateToken, async (req, res) => {
  try {
    const portfolioId = req.params.id;
    const { symbol, side, quantity, price, strategySignal, notes } = req.body;

    if (!symbol || !side || !quantity || !price) {
      return res.status(400).json({ error: 'All trade data must be provided.' });
    }

    if (!['buy', 'sell'].includes(side)) {
      return res.status(400).json({ error: 'Trade side must be "buy" or "sell".' });
    }

    const portfolio = await knex('paper_portfolios')
      .where({ id: portfolioId, user_id: req.user.userId, status: 'active' })
      .first();

    if (!portfolio) {
      return res.status(404).json({ error: 'Portfolio not found or is not active.' });
    }

    const totalAmount = quantity * price;
    const fees = totalAmount * 0.001; // 0.1% fee
    const totalCost = totalAmount + fees;

    if (side === 'buy' && portfolio.current_balance < totalCost) {
      return res.status(400).json({ error: 'Insufficient balance to complete the trade.' });
    }

    await knex('paper_trades').insert({
      portfolio_id: portfolioId,
      symbol: symbol.toUpperCase(),
      side,
      quantity,
      price,
      total_amount: totalAmount,
      fees,
      strategy_signal: strategySignal,
      notes
    });

    const newBalance = side === 'buy' ?
      portfolio.current_balance - totalCost :
      portfolio.current_balance + (totalAmount - fees);

    await knex('paper_portfolios').where({ id: portfolioId }).update({
      current_balance: newBalance,
      updated_at: knex.fn.now()
    });

    res.json({
      message: `Trade (${side}) executed successfully.`,
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
    console.error(error);
    res.status(500).json({ error: 'Failed to execute trade.' });
  }
});

// Get trade history for a portfolio
router.get('/:id/trades', authenticateToken, async (req, res) => {
  try {
    const portfolioId = req.params.id;
    const { page = 1, limit = 20 } = req.query;
    const offset = (page - 1) * limit;

    const portfolio = await knex('paper_portfolios')
      .where({ id: portfolioId, user_id: req.user.userId })
      .first();

    if (!portfolio) {
      return res.status(404).json({ error: 'Portfolio not found.' });
    }

    const trades = await knex('paper_trades')
      .where({ portfolio_id: portfolioId })
      .orderBy('executed_at', 'desc')
      .limit(limit)
      .offset(offset);

    const totalCountResult = await knex('paper_trades').where({ portfolio_id: portfolioId }).count({ count: '*' }).first();
    const totalCount = totalCountResult.count;


    res.json({
      trades,
      portfolio: {
        name: portfolio.name,
        current_balance: portfolio.current_balance,
        initial_balance: portfolio.initial_balance
      },
      pagination: {
        currentPage: parseInt(page),
        totalPages: Math.ceil(totalCount / limit),
        totalCount: parseInt(totalCount),
        limit: parseInt(limit)
      }
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to fetch trades.' });
  }
});

// Delete a portfolio
router.delete('/:id', authenticateToken, async (req, res) => {
  try {
    const portfolioId = req.params.id;

    const portfolio = await knex('paper_portfolios')
      .where({ id: portfolioId, user_id: req.user.userId })
      .first();

    if (!portfolio) {
      return res.status(404).json({ error: 'Portfolio not found.' });
    }

    await knex('paper_trades').where({ portfolio_id: portfolioId }).del();
    await knex('paper_portfolios').where({ id: portfolioId }).del();

    res.json({ message: 'Portfolio and all its trades have been deleted successfully.' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to delete portfolio.' });
  }
});

// Reset a portfolio (reset balance to initial value)
router.post('/:id/reset', authenticateToken, async (req, res) => {
  try {
    const portfolioId = req.params.id;

    const portfolio = await knex('paper_portfolios')
      .where({ id: portfolioId, user_id: req.user.userId })
      .first();

    if (!portfolio) {
      return res.status(404).json({ error: 'Portfolio not found.' });
    }

    // Delete all trades associated with the portfolio
    await knex('paper_trades').where({ portfolio_id: portfolioId }).del();

    // Reset the balance
    await knex('paper_portfolios')
      .where({ id: portfolioId })
      .update({
        current_balance: knex.raw('initial_balance'),
        updated_at: knex.fn.now()
      });

    res.json({
      message: 'Portfolio has been reset successfully.',
      balance: portfolio.initial_balance
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to reset portfolio.' });
  }
});

export default router;