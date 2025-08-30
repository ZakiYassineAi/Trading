import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { initializeDatabase } from './models/database.js';
import { errorHandler } from './middleware/errorHandler.js';
import { securityMiddleware } from './middleware/security.js';
import logger from './config/logger.js';
import { auditLogger } from './middleware/auditLogger.js';
import { authenticateToken } from './middleware/authMiddleware.js';
import { apiLimiter, authLimiter } from './middleware/rateLimiter.js';

// Import routes
import authRoutes from './routes/auth.js';
import strategiesRoutes from './routes/strategies.js';
import backtestRoutes from './routes/backtest.js';
import portfolioRoutes from './routes/portfolio.js';
import dataRoutes from './routes/data.js';
import alertsRoutes from './routes/alerts.js';
import defiRoutes from './routes/defi.js';
import swaggerUi from 'swagger-ui-express';
import YAML from 'yamljs';

// Configure __dirname for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Critical Security Check - منع التداول الحقيقي
if (process.env.ENABLE_LIVE_TRADING === 'true') {
  logger.error('❌ CRITICAL SECURITY ALERT: ENABLE_LIVE_TRADING is set to true!');
  process.exit(1);
}

logger.info('🔒 Security System: Paper Trading Only - Live trading is disabled.');

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

// Setup Swagger
const swaggerDocument = YAML.load('./openapi.yaml');
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

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

// Apply rate limiting
app.use('/api/', apiLimiter);
app.use('/api/auth', authLimiter, authRoutes);

// API Routes that require authentication
app.use('/api/strategies', authenticateToken, strategiesRoutes);
app.use('/api/backtest', authenticateToken, backtestRoutes);
app.use('/api/portfolio', authenticateToken, portfolioRoutes);
app.use('/api/data', authenticateToken, dataRoutes);
app.use('/api/alerts', authenticateToken, alertsRoutes);
app.use('/api/defi', authenticateToken, defiRoutes);

// Error handling
app.use(errorHandler);

// Initialize database and start server
async function startServer() {
  try {
    await initializeDatabase();
    logger.info('✅ Database initialized successfully.');

    app.listen(PORT, () => {
      logger.info(`🚀 Server running on port ${PORT}`);
      logger.info(`📊 Dashboard available at: http://localhost:5173`);
      logger.info(`🔧 API available at: http://localhost:${PORT}`);
      logger.info('🛡️  Paper Trading Mode Only - System is secure.');
    });
  } catch (error) {
    logger.error(`❌ Failed to start server: ${error.message}`);
    process.exit(1);
  }
}

startServer();

export default app;