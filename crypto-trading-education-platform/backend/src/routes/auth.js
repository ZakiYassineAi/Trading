import express from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { db } from '../models/database.js';

const router = express.Router();

// تسجيل مستخدم جديد (للتجربة فقط)
router.post('/register', async (req, res) => {
  try {
    const { username, email, password, fullName } = req.body;

    if (!username || !email || !password) {
      return res.status(400).json({
        error: 'يجب إدخال جميع البيانات المطلوبة'
      });
    }

    // تشفير كلمة المرور
    const passwordHash = await bcrypt.hash(password, 10);

    // إضافة المستخدم
    const result = await db.run(`
      INSERT INTO users (username, email, password_hash, full_name)
      VALUES (?, ?, ?, ?)
    `, [username, email, passwordHash, fullName || username]);

    // إنشاء محفظة افتراضية
    await db.run(`
      INSERT INTO paper_portfolios (user_id, name, initial_balance, current_balance)
      VALUES (?, ?, 10000.00, 10000.00)
    `, [result.lastID, `محفظة ${username} الرئيسية`]);

    res.status(201).json({
      message: 'تم إنشاء الحساب بنجاح',
      userId: result.lastID,
      paperTradingEnabled: true
    });
  } catch (error) {
    if (error.code === 'SQLITE_CONSTRAINT') {
      return res.status(400).json({
        error: 'اسم المستخدم أو البريد الإلكتروني مستخدم مسبقاً'
      });
    }
    throw error;
  }
});

// تسجيل الدخول
router.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.status(400).json({
        error: 'يجب إدخال اسم المستخدم وكلمة المرور'
      });
    }

    // البحث عن المستخدم
    const user = await db.get(`
      SELECT * FROM users WHERE username = ? OR email = ?
    `, [username, username]);

    if (!user || !user.is_active) {
      return res.status(401).json({
        error: 'بيانات تسجيل الدخول غير صحيحة'
      });
    }

    // التحقق من كلمة المرور
    const validPassword = await bcrypt.compare(password, user.password_hash);
    if (!validPassword) {
      return res.status(401).json({
        error: 'بيانات تسجيل الدخول غير صحيحة'
      });
    }

    // إنشاء JWT token
    const token = jwt.sign(
      {
        userId: user.id,
        username: user.username,
        paperTradingOnly: true
      },
      process.env.JWT_SECRET || 'default_secret_for_demo',
      { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
    );

    // تحديث وقت آخر دخول
    await db.run(`
      UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = ?
    `, [user.id]);

    res.json({
      message: 'تم تسجيل الدخول بنجاح',
      token,
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        fullName: user.full_name,
        preferences: JSON.parse(user.preferences || '{}'),
        paperTradingOnly: true,
        liveTradingDisabled: true
      }
    });
  } catch (error) {
    throw error;
  }
});

// الحصول على بيانات المستخدم الحالي
router.get('/me', authenticateToken, async (req, res) => {
  try {
    const user = await db.get(`
      SELECT id, username, email, full_name, preferences, created_at
      FROM users WHERE id = ?
    `, [req.user.userId]);

    if (!user) {
      return res.status(404).json({ error: 'المستخدم غير موجود' });
    }

    res.json({
      user: {
        ...user,
        preferences: JSON.parse(user.preferences || '{}'),
        paperTradingOnly: true,
        liveTradingDisabled: true
      }
    });
  } catch (error) {
    throw error;
  }
});

// Middleware للتحقق من JWT token
export function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'توكن الاعتماد مفقود' });
  }

  jwt.verify(token, process.env.JWT_SECRET || 'default_secret_for_demo', (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'توكن غير صالح' });
    }
    req.user = user;
    next();
  });
}

export default router;