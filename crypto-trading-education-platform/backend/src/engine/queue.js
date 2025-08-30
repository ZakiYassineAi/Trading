import Queue from 'bull';

// It's better to create a new Redis client for Bull to avoid conflicts
// with the one used for general pub/sub or caching.
const queueRedisOptions = {
  redis: {
    host: process.env.REDIS_HOST || '127.0.0.1',
    port: process.env.REDIS_PORT || 6379,
  },
};

const tradeQueue = new Queue('high_priority_trades', queueRedisOptions);
const dataProcessingQueue = new Queue('market_data_processing', queueRedisOptions);
const aiPredictionQueue = new Queue('ai_predictions',queueRedisOptions);

// Add error listeners for robustness
tradeQueue.on('error', (error) => {
  console.error('Bull trade queue error:', error);
});

dataProcessingQueue.on('error', (error) => {
  console.error('Bull data processing queue error:', error);
});

aiPredictionQueue.on('error', (error) => {
  console.error('Bull AI prediction queue error:', error);
});

console.log('✅ Bull message queues initialized.');

export {
  tradeQueue,
  dataProcessingQueue,
  aiPredictionQueue
};
