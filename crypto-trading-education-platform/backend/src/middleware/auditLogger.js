import { db } from '../models/database.js';

// Audit logger middleware
export function auditLogger(req, res, next) {
  // تجاهل الطلبات البسيطة
  if (req.path.includes('/health') || req.method === 'GET' && req.path.includes('/data')) {
    return next();
  }

  const logData = {
    action: `${req.method} ${req.path}`,
    resource_type: req.path.split('/')[2] || 'unknown',
    ip_address: req.ip || req.connection.remoteAddress,
    user_agent: req.get('User-Agent') || '',
    timestamp: new Date().toISOString(),
    details: JSON.stringify({
      query: req.query,
      body: req.method !== 'GET' ? req.body : undefined
    })
  };

  // حفظ السجل في قاعدة البيانات
  db.run(`
    INSERT INTO audit_logs (action, resource_type, ip_address, user_agent, details, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
  `, [logData.action, logData.resource_type, logData.ip_address, logData.user_agent, logData.details, logData.timestamp])
  .catch(error => {
    console.error('خطأ في حفظ سجل التدقيق:', error);
  });

  next();
}