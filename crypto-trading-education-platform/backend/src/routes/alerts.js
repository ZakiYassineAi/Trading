import express from 'express';
import { db } from '../models/database.js';
import { authenticateToken } from './auth.js';

const router = express.Router();

// الحصول على جميع التنبيهات
router.get('/', authenticateToken, async (req, res) => {
  try {
    const { active = true, page = 1, limit = 20 } = req.query;
    const offset = (page - 1) * limit;

    let query = `
      SELECT * FROM trading_alerts WHERE user_id = ?
    `;
    let params = [req.user.userId];

    if (active !== 'all') {
      query += ` AND is_active = ?`;
      params.push(active === 'true' ? 1 : 0);
    }

    query += ` ORDER BY created_at DESC LIMIT ? OFFSET ?`;
    params.push(parseInt(limit), offset);

    const alerts = await db.all(query, params);

    const totalCount = await db.get(`
      SELECT COUNT(*) as count FROM trading_alerts
      WHERE user_id = ? ${active !== 'all' ? 'AND is_active = ?' : ''}
    `, active !== 'all' ? [req.user.userId, active === 'true' ? 1 : 0] : [req.user.userId]);

    const formattedAlerts = alerts.map(alert => ({
      ...alert,
      notification_methods: JSON.parse(alert.notification_methods || '[]')
    }));

    res.json({
      alerts: formattedAlerts,
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

// إنشاء تنبيه جديد
router.post('/', authenticateToken, async (req, res) => {
  try {
    const {
      symbol,
      alertType,
      conditionType,
      targetValue,
      message,
      notificationMethods = ['email']
    } = req.body;

    if (!symbol || !alertType || !conditionType || !targetValue) {
      return res.status(400).json({
        error: 'يجب إدخال جميع البيانات المطلوبة'
      });
    }

    const validConditions = ['price_above', 'price_below', 'volume_spike', 'technical_signal'];
    if (!validConditions.includes(conditionType)) {
      return res.status(400).json({
        error: 'نوع الشرط غير صالح'
      });
    }

    const result = await db.run(`
      INSERT INTO trading_alerts (
        user_id, symbol, alert_type, condition_type, target_value,
        message, notification_methods
      ) VALUES (?, ?, ?, ?, ?, ?, ?)
    `, [
      req.user.userId,
      symbol.toUpperCase(),
      alertType,
      conditionType,
      targetValue,
      message || `تنبيه ${alertType} لعملة ${symbol.toUpperCase()}`,
      JSON.stringify(notificationMethods)
    ]);

    const alert = await db.get(`
      SELECT * FROM trading_alerts WHERE id = ?
    `, [result.lastID]);

    res.status(201).json({
      message: 'تم إنشاء التنبيه بنجاح',
      alert: {
        ...alert,
        notification_methods: JSON.parse(alert.notification_methods)
      }
    });
  } catch (error) {
    throw error;
  }
});

// تحديث تنبيه
router.put('/:id', authenticateToken, async (req, res) => {
  try {
    const alertId = req.params.id;
    const { targetValue, message, isActive, notificationMethods } = req.body;

    // التحقق من ملكية التنبيه
    const alert = await db.get(`
      SELECT * FROM trading_alerts WHERE id = ? AND user_id = ?
    `, [alertId, req.user.userId]);

    if (!alert) {
      return res.status(404).json({
        error: 'التنبيه غير موجود'
      });
    }

    await db.run(`
      UPDATE trading_alerts
      SET target_value = ?, message = ?, is_active = ?, notification_methods = ?
      WHERE id = ?
    `, [
      targetValue || alert.target_value,
      message || alert.message,
      isActive !== undefined ? (isActive ? 1 : 0) : alert.is_active,
      JSON.stringify(notificationMethods || JSON.parse(alert.notification_methods)),
      alertId
    ]);

    const updatedAlert = await db.get(`
      SELECT * FROM trading_alerts WHERE id = ?
    `, [alertId]);

    res.json({
      message: 'تم تحديث التنبيه بنجاح',
      alert: {
        ...updatedAlert,
        notification_methods: JSON.parse(updatedAlert.notification_methods)
      }
    });
  } catch (error) {
    throw error;
  }
});

// حذف تنبيه
router.delete('/:id', authenticateToken, async (req, res) => {
  try {
    const alertId = req.params.id;

    const alert = await db.get(`
      SELECT * FROM trading_alerts WHERE id = ? AND user_id = ?
    `, [alertId, req.user.userId]);

    if (!alert) {
      return res.status(404).json({
        error: 'التنبيه غير موجود'
      });
    }

    await db.run(`DELETE FROM trading_alerts WHERE id = ?`, [alertId]);

    res.json({ message: 'تم حذف التنبيه بنجاح' });
  } catch (error) {
    throw error;
  }
});

// تفعيل/إلغاء جميع التنبيهات
router.post('/toggle-all', authenticateToken, async (req, res) => {
  try {
    const { isActive } = req.body;

    await db.run(`
      UPDATE trading_alerts SET is_active = ? WHERE user_id = ?
    `, [isActive ? 1 : 0, req.user.userId]);

    const updatedCount = await db.get(`
      SELECT COUNT(*) as count FROM trading_alerts WHERE user_id = ?
    `, [req.user.userId]);

    res.json({
      message: `تم ${isActive ? 'تفعيل' : 'إلغاء'} جميع التنبيهات`,
      affected_count: updatedCount.count
    });
  } catch (error) {
    throw error;
  }
});

// فحص التنبيهات (يتم استدعاؤه بشكل دوري)
router.post('/check', async (req, res) => {
  try {
    // فحص التنبيهات النشطة غير المفعّلة
    const activeAlerts = await db.all(`
      SELECT * FROM trading_alerts
      WHERE is_active = 1 AND is_triggered = 0
    `);

    const triggeredAlerts = [];

    for (const alert of activeAlerts) {
      // محاكاة فحص الشروط (في البيئة الحقيقية ستحتاج لجلب البيانات الحالية)
      const shouldTrigger = Math.random() < 0.1; // 10% احتمال للتفعيل (محاكاة)

      if (shouldTrigger) {
        // تفعيل التنبيه
        await db.run(`
          UPDATE trading_alerts
          SET is_triggered = 1, triggered_at = CURRENT_TIMESTAMP,
              current_value = ?
          WHERE id = ?
        `, [alert.target_value * (0.9 + Math.random() * 0.2), alert.id]); // قيمة حالية محاكاة

        triggeredAlerts.push({
          id: alert.id,
          symbol: alert.symbol,
          alert_type: alert.alert_type,
          condition_type: alert.condition_type,
          target_value: alert.target_value,
          message: alert.message
        });
      }
    }

    res.json({
      checked_alerts: activeAlerts.length,
      triggered_alerts: triggeredAlerts,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    throw error;
  }
});

// إعادة تعيين تنبيه مفعّل
router.post('/:id/reset', authenticateToken, async (req, res) => {
  try {
    const alertId = req.params.id;

    const alert = await db.get(`
      SELECT * FROM trading_alerts WHERE id = ? AND user_id = ?
    `, [alertId, req.user.userId]);

    if (!alert) {
      return res.status(404).json({
        error: 'التنبيه غير موجود'
      });
    }

    await db.run(`
      UPDATE trading_alerts
      SET is_triggered = 0, triggered_at = NULL, current_value = NULL
      WHERE id = ?
    `, [alertId]);

    res.json({ message: 'تم إعادة تعيين التنبيه بنجاح' });
  } catch (error) {
    throw error;
  }
});

export default router;