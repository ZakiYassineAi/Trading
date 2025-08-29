import sqlite3 from 'sqlite3';
import { promisify } from 'util';
import path from 'path';
import fs from 'fs/promises';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const dbPath = process.env.DB_PATH || path.join(__dirname, '../database/trading_platform.db');

// Create database directory if it doesn't exist
const dbDir = path.dirname(dbPath);
try {
  await fs.mkdir(dbDir, { recursive: true });
} catch (error) {
  // Directory already exists
}

const db = new sqlite3.Database(dbPath);

// Promisify database methods
db.run = promisify(db.run.bind(db));
db.get = promisify(db.get.bind(db));
db.all = promisify(db.all.bind(db));

// Database initialization
export async function initializeDatabase() {
  try {
    // Enable foreign keys
    await db.run('PRAGMA foreign_keys = ON');

    // Create tables
    await createTables();
    await insertSampleData();

    console.log('قاعدة البيانات جاهزة');
  } catch (error) {
    console.error('خطأ في تهيئة قاعدة البيانات:', error);
    throw error;
  }
}

async function createTables() {
  const tables = [
    `
    CREATE TABLE IF NOT EXISTS users (
      id TEXT PRIMARY KEY DEFAULT (hex(randomblob(16))),
      username TEXT UNIQUE NOT NULL,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      full_name TEXT,
      avatar_url TEXT,
      is_active BOOLEAN DEFAULT 1,
      preferences TEXT DEFAULT '{"language":"ar","currency":"USD","timezone":"UTC"}',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    `,
    `
    CREATE TABLE IF NOT EXISTS trading_strategies (
      id TEXT PRIMARY KEY DEFAULT (hex(randomblob(16))),
      user_id TEXT,
      name TEXT NOT NULL,
      type TEXT NOT NULL CHECK (type IN ('SMA', 'EMA', 'RSI', 'MACD', 'BREAKOUT', 'ATR', 'MEAN_REVERSION', 'VOLATILITY_TARGETING')),
      parameters TEXT NOT NULL,
      description TEXT,
      is_active BOOLEAN DEFAULT 1,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    `,
    `
    CREATE TABLE IF NOT EXISTS backtest_results (
      id TEXT PRIMARY KEY DEFAULT (hex(randomblob(16))),
      user_id TEXT NOT NULL,
      strategy_id TEXT,
      symbol TEXT NOT NULL,
      timeframe TEXT NOT NULL,
      start_date DATE NOT NULL,
      end_date DATE NOT NULL,
      initial_capital DECIMAL(15,2) NOT NULL,
      final_capital DECIMAL(15,2) NOT NULL,
      total_return DECIMAL(10,4),
      cagr DECIMAL(10,4),
      sharpe_ratio DECIMAL(10,4),
      sortino_ratio DECIMAL(10,4),
      max_drawdown DECIMAL(10,4),
      calmar_ratio DECIMAL(10,4),
      hit_rate DECIMAL(10,4),
      total_trades INTEGER,
      winning_trades INTEGER,
      losing_trades INTEGER,
      metrics TEXT,
      equity_curve TEXT,
      trade_log TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    `,
    `
    CREATE TABLE IF NOT EXISTS paper_portfolios (
      id TEXT PRIMARY KEY DEFAULT (hex(randomblob(16))),
      user_id TEXT NOT NULL,
      name TEXT NOT NULL,
      initial_balance DECIMAL(15,2) NOT NULL DEFAULT 10000,
      current_balance DECIMAL(15,2) NOT NULL DEFAULT 10000,
      currency TEXT DEFAULT 'USD',
      status TEXT DEFAULT 'active' CHECK (status IN ('active', 'paused', 'closed')),
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    `,
    `
    CREATE TABLE IF NOT EXISTS paper_trades (
      id TEXT PRIMARY KEY DEFAULT (hex(randomblob(16))),
      portfolio_id TEXT NOT NULL,
      symbol TEXT NOT NULL,
      side TEXT NOT NULL CHECK (side IN ('buy', 'sell')),
      quantity DECIMAL(20,8) NOT NULL,
      price DECIMAL(15,8) NOT NULL,
      total_amount DECIMAL(15,2) NOT NULL,
      fees DECIMAL(15,2) DEFAULT 0,
      status TEXT DEFAULT 'filled' CHECK (status IN ('pending', 'filled', 'cancelled')),
      strategy_signal TEXT,
      notes TEXT,
      executed_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    `,
    `
    CREATE TABLE IF NOT EXISTS crypto_data (
      id TEXT PRIMARY KEY DEFAULT (hex(randomblob(16))),
      symbol TEXT NOT NULL,
      price DECIMAL(15,8) NOT NULL,
      volume_24h DECIMAL(20,2),
      market_cap DECIMAL(20,2),
      price_change_24h DECIMAL(10,4),
      timestamp DATETIME NOT NULL,
      timeframe TEXT NOT NULL DEFAULT '1d',
      ohlc TEXT,
      technical_indicators TEXT,
      last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    `,
    `
    CREATE TABLE IF NOT EXISTS trading_alerts (
      id TEXT PRIMARY KEY DEFAULT (hex(randomblob(16))),
      user_id TEXT NOT NULL,
      symbol TEXT NOT NULL,
      alert_type TEXT NOT NULL,
      condition_type TEXT NOT NULL CHECK (condition_type IN ('price_above', 'price_below', 'volume_spike', 'technical_signal')),
      target_value DECIMAL(15,8),
      current_value DECIMAL(15,8),
      message TEXT,
      is_triggered BOOLEAN DEFAULT 0,
      is_active BOOLEAN DEFAULT 1,
      notification_methods TEXT DEFAULT '["email"]',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      triggered_at DATETIME
    )
    `,
    `
    CREATE TABLE IF NOT EXISTS audit_logs (
      id TEXT PRIMARY KEY DEFAULT (hex(randomblob(16))),
      user_id TEXT,
      action TEXT NOT NULL,
      resource_type TEXT,
      resource_id TEXT,
      details TEXT,
      ip_address TEXT,
      user_agent TEXT,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
      severity TEXT DEFAULT 'info' CHECK (severity IN ('info', 'warning', 'error', 'critical'))
    )
    `,
    `
    CREATE TABLE IF NOT EXISTS defi_simulations (
      id TEXT PRIMARY KEY DEFAULT (hex(randomblob(16))),
      user_id TEXT NOT NULL,
      protocol_name TEXT NOT NULL,
      simulation_type TEXT NOT NULL CHECK (simulation_type IN ('staking', 'yield_farming', 'liquidity_pool')),
      token_symbol TEXT NOT NULL,
      amount DECIMAL(20,8) NOT NULL,
      simulated_apy DECIMAL(10,4) NOT NULL,
      duration_days INTEGER NOT NULL,
      projected_returns DECIMAL(15,2),
      start_date DATE NOT NULL,
      end_date DATE,
      status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled')),
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    `
  ];

  for (const table of tables) {
    await db.run(table);
  }
}

async function insertSampleData() {
  // Insert sample user
  const sampleUser = {
    id: 'user_001',
    username: 'demo_trader',
    email: 'demo@trading-platform.com',
    password_hash: '$2b$10$example.hash.for.demo.user',
    full_name: 'متداول تجريبي',
    is_active: 1
  };

  try {
    await db.run(`
      INSERT OR IGNORE INTO users (id, username, email, password_hash, full_name, is_active)
      VALUES (?, ?, ?, ?, ?, ?)
    `, [sampleUser.id, sampleUser.username, sampleUser.email, sampleUser.password_hash, sampleUser.full_name, sampleUser.is_active]);

    // Insert sample strategies
    const sampleStrategies = [
      {
        id: 'strategy_001',
        user_id: 'user_001',
        name: 'استراتيجية Moving Average البسيطة',
        type: 'SMA',
        parameters: JSON.stringify({ fast: 10, slow: 30, symbol: 'BTC' }),
        description: 'استراتيجية تقاطع المتوسط المتحرك البسيط'
      },
      {
        id: 'strategy_002',
        user_id: 'user_001',
        name: 'استراتيجية RSI التقليدية',
        type: 'RSI',
        parameters: JSON.stringify({ period: 14, oversold: 30, overbought: 70, symbol: 'ETH' }),
        description: 'استراتيجية مؤشر القوة النسبية'
      }
    ];

    for (const strategy of sampleStrategies) {
      await db.run(`
        INSERT OR IGNORE INTO trading_strategies (id, user_id, name, type, parameters, description)
        VALUES (?, ?, ?, ?, ?, ?)
      `, [strategy.id, strategy.user_id, strategy.name, strategy.type, strategy.parameters, strategy.description]);
    }

    // Insert sample portfolio
    await db.run(`
      INSERT OR IGNORE INTO paper_portfolios (id, user_id, name, initial_balance, current_balance)
      VALUES ('portfolio_001', 'user_001', 'محفظة تجريبية رئيسية', 10000.00, 10000.00)
    `);

    console.log('تم إدراج البيانات التجريبية');
  } catch (error) {
    console.log('البيانات التجريبية موجودة مسبقاً');
  }
}

export { db };