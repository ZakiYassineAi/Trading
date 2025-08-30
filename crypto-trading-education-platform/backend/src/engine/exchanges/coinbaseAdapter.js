import ExchangeAdapter from './baseAdapter.js';
import WebSocket from 'ws';

class CoinbaseAdapter extends ExchangeAdapter {
  constructor() {
    super('Coinbase');
    this.apiUrl = 'wss://ws-feed.pro.coinbase.com';
  }

  connect() {
    console.log(`Connecting to ${this.name}...`);
    // Logic to connect to Coinbase WebSocket will be implemented here.
    this.emit('connected');
  }

  subscribeToTicker(symbol) {
    console.log(`Subscribing to ${symbol} ticker on ${this.name}`);
    // Subscription logic will be implemented here.
  }

  subscribeToOrderBook(symbol) {
    console.log(`Subscribing to ${symbol} order book on ${this.name}`);
    // Subscription logic will be implemented here.
  }
}

export default CoinbaseAdapter;
