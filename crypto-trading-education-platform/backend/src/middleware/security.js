import { db } from '../models/database.js';

// Security middleware - منع التداول الحقيقي
export function securityMiddleware(req, res, next) {
  // إضافة headers أمنية
  res.setHeader('X-Trading-Mode', 'PAPER_ONLY');
  res.setHeader('X-Live-Trading-Disabled', 'true');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // منع أي طلب يحتوي على كلمات تدل على التداول الحقيقي
  const dangerousKeywords = ['live_trade', 'real_order', 'execute_trade', 'live_api_key'];
  const requestBody = JSON.stringify(req.body || {}).toLowerCase();
  const requestPath = req.path.toLowerCase();

  for (const keyword of dangerousKeywords) {
    if (requestBody.includes(keyword) || requestPath.includes(keyword)) {
      return res.status(403).json({
        error: 'تم منع العملية - النظام يعمل في وضع Paper Trading فقط',
        code: 'LIVE_TRADING_BLOCKED',
        timestamp: new Date().toISOString()
      });
    }
  }

  next();
}