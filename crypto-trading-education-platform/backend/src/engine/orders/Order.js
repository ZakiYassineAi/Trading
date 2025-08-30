import { v4 as uuidv4 } from 'uuid';
import { OrderStatus } from './orderTypes.js';

class Order {
  constructor({ symbol, type, side, amount, price = null, stopPrice = null }) {
    if (!symbol || !type || !side || !amount) {
      throw new Error('Symbol, type, side, and amount are required for an order.');
    }

    this.id = uuidv4();
    this.symbol = symbol;
    this.type = type;
    this.side = side;
    this.amount = amount;
    this.price = price;
    this.stopPrice = stopPrice;
    this.status = OrderStatus.PENDING;
    this.createdAt = new Date();
    this.updatedAt = new Date();
  }

  // Method to update order status
  updateStatus(newStatus) {
    this.status = newStatus;
    this.updatedAt = new Date();
  }

  // Method to serialize order data
  toObject() {
    return {
      id: this.id,
      symbol: this.symbol,
      type: this.type,
      side: this.side,
      amount: this.amount,
      price: this.price,
      stopPrice: this.stopPrice,
      status: this.status,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}

export default Order;
