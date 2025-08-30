import { knex } from '../models/database.js';

// Audit logger middleware
export function auditLogger(req, res, next) {
  // Ignore simple requests
  if (req.path.includes('/health') || (req.method === 'GET' && req.path.includes('/data'))) {
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

  // Save the log to the database
  knex('audit_logs').insert(logData)
    .catch(error => {
      console.error('Error saving audit log:', error);
    });

  next();
}