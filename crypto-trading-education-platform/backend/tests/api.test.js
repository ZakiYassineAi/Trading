import request from 'supertest';
import app from '../src/index.js'; // Adjust the path to your Express app

// Mock the initializeDatabase function to prevent it from running in tests
jest.mock('../src/models/database.js', () => ({
  initializeDatabase: jest.fn().mockResolvedValue(true),
}));

describe('API Health Check', () => {
  it('should return 200 OK for GET /health', async () => {
    const response = await request(app).get('/health');
    expect(response.statusCode).toBe(200);
    expect(response.body.status).toBe('healthy');
    expect(response.body.paperTradingOnly).toBe(true);
  });
});

describe('API Security', () => {
  it('should return 401 Unauthorized for a protected route without a token', async () => {
    const response = await request(app).get('/api/strategies');
    expect(response.statusCode).toBe(401);
  });
});
