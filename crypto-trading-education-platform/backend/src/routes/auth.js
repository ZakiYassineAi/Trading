import express from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { db } from '../models/database.js';
import crypto from 'crypto';

const router = express.Router();

// Helper function to generate tokens
const generateTokens = (user) => {
  const accessToken = jwt.sign(
    { userId: user.id, username: user.username, role: user.role },
    process.env.JWT_SECRET || 'default_secret',
    { expiresIn: '15m' }
  );
  const refreshToken = crypto.randomBytes(40).toString('hex');
  return { accessToken, refreshToken };
};

// Login
router.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    const user = await db.knex('users').where({ username }).orWhere({ email: username }).first();

    if (!user || !await bcrypt.compare(password, user.password_hash)) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const { accessToken, refreshToken } = generateTokens(user);
    const expiryDate = new Date();
    expiryDate.setDate(expiryDate.getDate() + 30);

    await db.saveTokens(user.id, {
      accesstoken: accessToken,
      refreshtoken: refreshToken,
      idtoken: 'not_implemented',
      expireson: expiryDate.toISOString()
    });

    res.json({
      message: 'Logged in successfully',
      accessToken,
      refreshToken,
      user: { id: user.id, username: user.username, role: user.role }
    });

  } catch (error) {
    res.status(500).json({ error: 'An error occurred' });
  }
});

// Refresh Token
router.post('/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  if (!refreshToken) {
    return res.sendStatus(401);
  }

  // In a real app, you would have a separate table for refresh tokens
  // and you would validate them more securely.
  // This is a simplified implementation.
  const users = await db.getUsers();
  const userRecord = users.find(u => {
    const tokens = u.tokens ? JSON.parse(u.tokens) : {};
    return tokens.refreshtoken === refreshToken;
  });

  if (!userRecord) {
    return res.sendStatus(403);
  }

  const { accessToken } = generateTokens(userRecord);
  res.json({ accessToken });
});

// Logout
router.post('/logout', async (req, res) => {
  // This is a simplified implementation.
  // In a real app, you would invalidate the refresh token in the database.
  res.json({ message: 'Logged out successfully' });
});


// Middleware to authenticate token
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (token == null) return res.sendStatus(401);

  jwt.verify(token, process.env.JWT_SECRET || 'default_secret', (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
};

const requireAuth = authenticateToken;

// Middleware for role-based access control
const requireRole = (role) => {
  return (req, res, next) => {
    if (req.user && req.user.role === role) {
      next();
    } else {
      res.status(403).json({ error: 'Forbidden' });
    }
  };
};

// Example of a protected route for admins
router.get('/admin', requireAuth, requireRole('admin'), (req, res) => {
  res.json({ message: 'Welcome, admin!' });
});


export default router;
