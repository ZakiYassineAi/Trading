import express from 'express';
import axios from 'axios';
import { knex } from '../models/database.js';
import { authenticateToken } from './auth.js';

const router = express.Router();

// Get current cryptocurrency data
router.get('/crypto/current', async (req, res) => {
  try {
    const { symbols = 'bitcoin,ethereum,cardano,polygon,chainlink,solana,avalanche-2,polkadot' } = req.query;

    // Attempt to fetch live data from CoinGecko
    try {
      const coingeckoResponse = await axios.get(
        `https://api.coingecko.com/api/v3/simple/price?ids=${symbols}&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true&include_market_cap=true`,
        { timeout: 5000 }
      );

      const formattedData = Object.keys(coingeckoResponse.data).map(key => {
        const data = coingeckoResponse.data[key];
        return {
          symbol: key.toUpperCase(),
          name: key.charAt(0).toUpperCase() + key.slice(1).replace(/-/g, ' '),
          price: data.usd,
          price_change_24h: data.usd_24h_change || 0,
          volume_24h: data.usd_24h_vol || 0,
          market_cap: data.usd_market_cap || 0,
        };
      });

      // Save the data to the database (upsert)
      for (const crypto of formattedData) {
        await knex('crypto_data')
          .insert({
            symbol: crypto.symbol,
            price: crypto.price,
            volume_24h: crypto.volume_24h,
            market_cap: crypto.market_cap,
            price_change_24h: crypto.price_change_24h,
          })
          .onConflict('symbol')
          .merge();
      }

      res.json({ data: formattedData, source: 'coingecko' });

    } catch (apiError) {
      console.error('CoinGecko API error:', apiError.message);

      // In case of API failure, return mock data
      const mockData = generateMockCryptoData();
      res.json({ data: mockData, source: 'mock', note: 'CoinGecko API is unavailable' });
    }
  } catch (error) {
    console.error('Error fetching crypto data:', error);
    res.status(500).json({ error: 'Failed to fetch crypto data.' });
  }
});

// Get historical data for a specific cryptocurrency
router.get('/crypto/history/:symbol', async (req, res) => {
  try {
    const { symbol } = req.params;
    const { timeframe = '1d', limit = 100 } = req.query;

    // Attempt to fetch historical data from CoinGecko
    try {
      const days = timeframe === '1h' ? 1 : timeframe === '1d' ? 90 : 365;
      const coingeckoResponse = await axios.get(
        `https://api.coingecko.com/api/v3/coins/${symbol.toLowerCase()}/market_chart?vs_currency=usd&days=${days}&interval=${timeframe === '1h' ? 'hourly' : 'daily'}`,
        { timeout: 10000 }
      );

      const prices = coingeckoResponse.data.prices.slice(-limit);
      const volumes = coingeckoResponse.data.total_volumes.slice(-limit);

      const formattedData = prices.map((price, index) => ({
        timestamp: new Date(price[0]).toISOString(),
        price: price[1],
        volume: volumes[index] ? volumes[index][1] : 0,
        symbol: symbol.toUpperCase()
      }));

      res.json({
        data: formattedData,
        symbol: symbol.toUpperCase(),
        timeframe,
        source: 'coingecko'
      });

    } catch (apiError) {
      console.error('CoinGecko history API error:', apiError.message);

      // Historical mock data
      const mockData = generateMockHistoricalData(symbol.toUpperCase(), timeframe, parseInt(limit));
      res.json({
        data: mockData,
        symbol: symbol.toUpperCase(),
        timeframe,
        source: 'mock',
        note: 'CoinGecko API is unavailable'
      });
    }
  } catch (error) {
    console.error('Error fetching historical data:', error);
    res.status(500).json({ error: 'Failed to fetch historical data.' });
  }
});

// Get OHLC data
router.get('/crypto/ohlc/:symbol', async (req, res) => {
  try {
    const { symbol } = req.params;
    const { timeframe = '1d', limit = 100 } = req.query;

    // Mock OHLC data (in a real environment, you would need a paid API)
    const ohlcData = generateMockOHLCData(symbol.toUpperCase(), timeframe, parseInt(limit));

    res.json({
      data: ohlcData,
      symbol: symbol.toUpperCase(),
      timeframe,
      source: 'mock'
    });
  } catch (error) {
    console.error('Error fetching OHLC data:', error);
    res.status(500).json({ error: 'Failed to fetch OHLC data.' });
  }
});

// Get top trending coins
router.get('/crypto/trending', async (req, res) => {
  try {
    try {
      const response = await axios.get(
        'https://api.coingecko.com/api/v3/search/trending',
        { timeout: 5000 }
      );

      const trending = response.data.coins.map(coin => ({
        id: coin.item.id,
        name: coin.item.name,
        symbol: coin.item.symbol,
        market_cap_rank: coin.item.market_cap_rank || 0,
        price_btc: coin.item.price_btc || 0
      }));

      res.json({ data: trending, source: 'coingecko' });

    } catch (apiError) {
      console.error('Trending API error:', apiError.message);

      const mockTrending = [
        { id: 'bitcoin', name: 'Bitcoin', symbol: 'BTC', market_cap_rank: 1, price_btc: 1.0 },
        { id: 'ethereum', name: 'Ethereum', symbol: 'ETH', market_cap_rank: 2, price_btc: 0.074 },
        { id: 'cardano', name: 'Cardano', symbol: 'ADA', market_cap_rank: 8, price_btc: 0.000012 },
        { id: 'solana', name: 'Solana', symbol: 'SOL', market_cap_rank: 5, price_btc: 0.002 },
        { id: 'chainlink', name: 'Chainlink', symbol: 'LINK', market_cap_rank: 12, price_btc: 0.0004 }
      ];

      res.json({ data: mockTrending, source: 'mock' });
    }
  } catch (error) {
    console.error('Error fetching trending coins:', error);
    res.status(500).json({ error: 'Failed to fetch trending coins.' });
  }
});

// Generate mock crypto data
function generateMockCryptoData() {
  const cryptos = [
    { symbol: 'BTC', name: 'Bitcoin', basePrice: 45000 },
    { symbol: 'ETH', name: 'Ethereum', basePrice: 3200 },
    { symbol: 'ADA', name: 'Cardano', basePrice: 0.52 },
    { symbol: 'MATIC', name: 'Polygon', basePrice: 0.95 },
    { symbol: 'LINK', name: 'Chainlink', basePrice: 18.5 },
    { symbol: 'SOL', name: 'Solana', basePrice: 95 },
    { symbol: 'AVAX', name: 'Avalanche', basePrice: 42 },
    { symbol: 'DOT', name: 'Polkadot', basePrice: 7.8 }
  ];

  return cryptos.map(crypto => {
    const priceVariation = (Math.random() - 0.5) * 0.1; // ±5% variation
    const currentPrice = crypto.basePrice * (1 + priceVariation);
    const change24h = (Math.random() - 0.5) * 10; // ±5% daily change

    return {
      symbol: crypto.symbol,
      name: crypto.name,
      price: Math.round(currentPrice * 100) / 100,
      price_change_24h: Math.round(change24h * 100) / 100,
      volume_24h: Math.round(Math.random() * 1000000000),
      market_cap: Math.round(currentPrice * (1000000 + Math.random() * 20000000)),
      last_updated: new Date().toISOString()
    };
  });
}

// Generate mock historical data
function generateMockHistoricalData(symbol, timeframe, limit) {
  const data = [];
  const basePrice = symbol === 'BTC' ? 45000 : symbol === 'ETH' ? 3200 : 100;
  const now = new Date();
  const intervalMs = timeframe === '1h' ? 60 * 60 * 1000 : 24 * 60 * 60 * 1000;

  for (let i = limit - 1; i >= 0; i--) {
    const timestamp = new Date(now.getTime() - (i * intervalMs));
    const randomWalk = (Math.random() - 0.5) * 0.03; // 3% random walk
    const price = basePrice * (1 + randomWalk * (limit - i) / limit);
    const volume = Math.random() * 1000000000;

    data.push({
      timestamp: timestamp.toISOString(),
      price: Math.round(price * 100) / 100,
      volume: Math.round(volume),
      symbol
    });
  }

  return data;
}

// Generate mock OHLC data
function generateMockOHLCData(symbol, timeframe, limit) {
  const data = [];
  const basePrice = symbol === 'BTC' ? 45000 : symbol === 'ETH' ? 3200 : 100;
  const now = new Date();
  const intervalMs = timeframe === '1h' ? 60 * 60 * 1000 : 24 * 60 * 60 * 1000;

  let lastClose = basePrice;

  for (let i = limit - 1; i >= 0; i--) {
    const timestamp = new Date(now.getTime() - (i * intervalMs));

    const open = lastClose;
    const volatility = 0.02; // 2% volatility
    const high = open * (1 + Math.random() * volatility);
    const low = open * (1 - Math.random() * volatility);
    const close = low + Math.random() * (high - low);
    const volume = Math.random() * 1000000000;

    data.push({
      timestamp: timestamp.toISOString(),
      open: Math.round(open * 100) / 100,
      high: Math.round(high * 100) / 100,
      low: Math.round(low * 100) / 100,
      close: Math.round(close * 100) / 100,
      volume: Math.round(volume),
      symbol
    });

    lastClose = close;
  }

  return data;
}

// Local data for backtesting
router.get('/backtest/:symbol', authenticateToken, async (req, res) => {
  try {
    const { symbol } = req.params;
    const { startDate, endDate, timeframe = '1d' } = req.query;

    if (!startDate || !endDate) {
      return res.status(400).json({
        error: 'Start and end date are required.'
      });
    }

    // This is a placeholder for fetching historical data from a local source
    const daysDiff = Math.ceil((new Date(endDate) - new Date(startDate)) / (1000 * 60 * 60 * 24));
    const historicalData = generateMockHistoricalData(symbol.toUpperCase(), timeframe, daysDiff);

    res.json({
      data: historicalData,
      symbol: symbol.toUpperCase(),
      timeframe,
      period: {
        start: startDate,
        end: endDate,
        days: daysDiff
      }
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to fetch backtest data.' });
  }
});

export default router;