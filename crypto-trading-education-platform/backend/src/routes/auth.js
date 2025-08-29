import express from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { db } from '../models/database.js';
import crypto from 'crypto';

const router = express.Router();

// Helper function to generate tokens
const generateTokens = (user) => {
  const accessToken = jwt.sign(
    { userId: user.id, username: user.username },
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
    expiryDate.setDate(expiryDate.getDate() + 30); // Refresh token expires in 30 days

    await db.saveTokens(user.id, {
      accesstoken: accessToken,
      refreshtoken: refreshToken,
      idtoken: 'not_implemented', // Placeholder for B2C id_token
      expireson: expiryDate.toISOString()
    });

    res.json({
      message: 'Logged in successfully',
      accessToken,
      refreshToken,
      user: { id: user.id, username: user.username }
    });

  } catch (error) {
    res.status(500).json({ error: 'An error occurred' });
  }
});

export default router;
