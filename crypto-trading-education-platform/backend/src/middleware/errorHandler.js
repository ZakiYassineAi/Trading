// Error handler middleware
export function errorHandler(error, req, res, next) {
  console.error('خطأ في الخادم:', error);

  // تسجيل الخطأ في قاعدة البيانات
  const errorLog = {
    action: 'ERROR',
    resource_type: 'system',
    details: JSON.stringify({
      message: error.message,
      stack: error.stack,
      url: req.url,
      method: req.method
    }),
    severity: 'error',
    timestamp: new Date().toISOString()
  };

  // حفظ السجل دون إيقاف العملية
  import('../models/database.js').then(({ db }) => {
    db.run(`
      INSERT INTO audit_logs (action, resource_type, details, severity, timestamp)
      VALUES (?, ?, ?, ?, ?)
    `, [errorLog.action, errorLog.resource_type, errorLog.details, errorLog.severity, errorLog.timestamp])
    .catch(dbError => {
      console.error('خطأ في حفظ سجل الخطأ:', dbError);
    });
  });

  // إرسال رد مناسب للمستخدم
  const isDevelopment = process.env.NODE_ENV === 'development';

  res.status(error.status || 500).json({
    error: 'حدث خطأ في الخادم',
    code: error.code || 'INTERNAL_SERVER_ERROR',
    message: isDevelopment ? error.message : 'خطأ داخلي في الخادم',
    timestamp: new Date().toISOString(),
    ...(isDevelopment && { stack: error.stack })
  });
}