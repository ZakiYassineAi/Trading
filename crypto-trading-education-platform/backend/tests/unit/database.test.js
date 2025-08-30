import { knex, redisClient } from '../../src/models/database.js';

jest.mock('knex', () => {
  const mKnex = () => ({
    migrate: {
      latest: jest.fn().mockResolvedValue(),
    },
    seed: {
      run: jest.fn().mockResolvedValue(),
    },
    select: jest.fn().mockReturnThis(),
    from: jest.fn().mockReturnThis(),
    where: jest.fn().mockReturnThis(),
    first: jest.fn().mockResolvedValue({}),
    insert: jest.fn().mockReturnThis(),
    returning: jest.fn().mockResolvedValue([{ id: 1 }]),
    update: jest.fn().mockResolvedValue(1),
    del: jest.fn().mockResolvedValue(1),
    raw: jest.fn(),
  });
  mKnex.raw = jest.fn();
  return mKnex;
});

jest.mock('redis', () => {
    const redis = jest.requireActual('redis');
    return {
        ...redis,
        createClient: jest.fn().mockReturnValue({
            on: jest.fn(),
            connect: jest.fn().mockResolvedValue(),
        }),
    };
});

describe('Database Module', () => {
  it('should export a knex instance', () => {
    expect(knex).toBeDefined();
  });

  it('should export a redis client instance', () => {
    expect(redisClient).toBeDefined();
    expect(redisClient.on).toHaveBeenCalledWith('error', expect.any(Function));
    expect(redisClient.connect).toHaveBeenCalled();
  });
});
