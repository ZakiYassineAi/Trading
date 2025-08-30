import request from 'supertest';
import app from '../../../src/index.js'; // Assuming your app is exported from index.js
import { knex } from '../../../src/models/database.js';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';



describe('Auth Routes', () => {
  beforeAll(async () => {
    await knex.migrate.latest();
  });

  afterAll(async () => {
    await knex.migrate.rollback();
  });

  beforeEach(async () => {
    // Clear all tables before each test
    await knex('users').truncate();
    // You might need to add other tables here if they have foreign key constraints
  });

  describe('POST /api/auth/register', () => {
    it('should register a new user successfully', async () => {
      const res = await request(app)
        .post('/api/auth/register')
        .send({
          username: 'testuser',
          email: 'test@example.com',
          password: 'password123',
        });

      expect(res.statusCode).toEqual(201);
      expect(res.body).toHaveProperty('message', 'User registered successfully.');
      expect(res.body).toHaveProperty('userId');
    });
  });

  describe('POST /api/auth/login', () => {
    it('should login an existing user and return tokens', async () => {
      // First, register a user
      await request(app)
        .post('/api/auth/register')
        .send({
          username: 'loginuser',
          email: 'login@example.com',
          password: 'password123',
        });

      // Then, try to login
      const res = await request(app)
        .post('/api/auth/login')
        .send({
          username: 'loginuser',
          password: 'password123',
        });

      expect(res.statusCode).toEqual(200);
      expect(res.body).toHaveProperty('accessToken');
      expect(res.body).toHaveProperty('refreshToken');
      expect(res.body.user).toHaveProperty('username', 'loginuser');
    });

    it('should return 401 for invalid credentials', async () => {
      const res = await request(app)
        .post('/api/auth/login')
        .send({
          username: 'nouser',
          password: 'wrongpassword',
        });

      expect(res.statusCode).toEqual(401);
      expect(res.body).toHaveProperty('error', 'Invalid credentials');
    });
  });
});
