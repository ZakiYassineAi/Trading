import EventEmitter from 'events';

class ExchangeAdapter extends EventEmitter {
  constructor(exchangeName) {
    super();
    this.name = exchangeName;
    this.ws = null;
  }

  connect() {
    throw new Error('connect() must be implemented by a subclass');
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }

  subscribeToTicker(symbol) {
    throw new Error('subscribeToTicker() must be implemented by a subclass');
  }

  subscribeToOrderBook(symbol) {
    throw new Error('subscribeToOrderBook() must be implemented by a subclass');
  }

  _handleMessage(message) {
    // Subclasses will implement their message handling logic
    // and emit standardized events like 'ticker' or 'orderBookUpdate'.
    // For example:
    // const data = JSON.parse(message);
    // this.emit('ticker', { exchange: this.name, symbol: data.s, price: data.p });
  }
}

export default ExchangeAdapter;
