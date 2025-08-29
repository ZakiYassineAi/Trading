import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { initializeDatabase } from './models/database.js';
import { errorHandler } from './middleware/errorHandler.js';
import { securityMiddleware } from './middleware/security.js';
import { auditLogger } from './middleware/auditLogger.js';

// Import routes
import authRoutes from './routes/auth.js';
import strategiesRoutes from './routes/strategies.js';
import backtestRoutes from './routes/backtest.js';
import portfolioRoutes from './routes/portfolio.js';
import dataRoutes from './routes/data.js';
import alertsRoutes from './routes/alerts.js';
import defiRoutes from './routes/defi.js';

// Configure __dirname for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Critical Security Check - منع التداول الحقيقي
if (process.env.ENABLE_LIVE_TRADING === 'true') {
  console.error('❌ خطأ أمني: ENABLE_LIVE_TRADING يجب أن يكون false دائماً');
  process.exit(1);
}

console.log('🔒 نظام الأمان: Paper Trading فقط - التداول الحقيقي معطل');

// Middleware
app.use(cors({
  origin: process.env.NODE_ENV === 'production'
    ? ['https://your-production-domain.com']
    : ['http://localhost:5173', 'http://localhost:3000'],
  credentials: true
}));

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Security middleware
app.use(securityMiddleware);
app.use(auditLogger);

// Static files
app.use('/data', express.static(join(__dirname, '../../public/data')));
app.use('/charts', express.static(join(__dirname, '../../public/charts')));

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV,
    paperTradingOnly: true,
    liveTradingDisabled: process.env.ENABLE_LIVE_TRADING !== 'true'
  });
});

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/strategies', strategiesRoutes);
app.use('/api/backtest', backtestRoutes);
app.use('/api/portfolio', portfolioRoutes);
app.use('/api/data', dataRoutes);
app.use('/api/alerts', alertsRoutes);
app.use('/api/defi', defiRoutes);

// Error handling
app.use(errorHandler);

// Initialize database and start server
async function startServer() {
  try {
    await initializeDatabase();
    console.log('✅ تم تهيئة قاعدة البيانات بنجاح');

    app.listen(PORT, () => {
      console.log(`🚀 الخادم يعمل على المنفذ ${PORT}`);
      console.log(`📊 لوحة التحكم: http://localhost:5173`);
      console.log(`🔧 API متاح على: http://localhost:${PORT}`);
      console.log('🛡️  وضع Paper Trading فقط - آمن تماماً');
    });
  } catch (error) {
    console.error('❌ خطأ في بدء الخادم:', error);
    process.exit(1);
  }
}

startServer();

export default app;