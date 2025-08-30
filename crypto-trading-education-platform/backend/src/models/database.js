import knexLib from 'knex';
import knexConfig from '../../knexfile.cjs';
import { createClient } from 'redis';

const env = process.env.NODE_ENV || 'development';

let knexInstance;
let redisInstance;

function getKnex() {
  if (!knexInstance) {
    knexInstance = knexLib(knexConfig[env]);
  }
  return knexInstance;
}

function getRedis() {
  if (!redisInstance) {
    redisInstance = createClient({
      url: process.env.REDIS_URL || 'redis://127.0.0.1:6379'
    });
    redisInstance.on('error', (err) => console.log('Redis Client Error', err));
    (async () => {
      try {
        await redisInstance.connect();
        console.log('✅ Connected to Redis successfully.');
      } catch (err) {
        console.error('❌ Could not connect to Redis:', err);
      }
    })();
  }
  return redisInstance;
}

export const knex = getKnex();
export const redisClient = getRedis();


// Database helper functions, now exported directly

// Get all users
export const getUsers = () => knex('users').select('*');

// Get a single user by ID
export const getUserById = (id) => knex('users').where({ id }).first();

// Save tokens for a user
export const saveTokens = async (userId, tokenObj) => {
  const tokensJson = JSON.stringify(tokenObj);
  return knex('users').where({ id: userId }).update({ tokens: tokensJson });
};

// Get tokens for a user
export const getTokens = async (userId) => {
  const row = await knex('users').where({ id: userId }).first('tokens');
  return row && row.tokens ? JSON.parse(row.tokens) : null;
};
