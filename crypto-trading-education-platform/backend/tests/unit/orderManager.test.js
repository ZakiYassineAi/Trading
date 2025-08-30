import orderManager from '../../src/engine/orders/orderManager.js';
import { OrderType, OrderSide, OrderStatus } from '../../src/engine/orders/orderTypes.js';
import { tradeQueue } from '../../src/engine/queue.js';
import { getIO } from '../../src/engine/websockets/socketServer.js';

jest.mock('../../src/engine/queue.js', () => ({
  tradeQueue: {
    add: jest.fn(),
    process: jest.fn(),
    on: jest.fn(),
  },
}));

const mockEmit = jest.fn();
jest.mock('../../src/engine/websockets/socketServer.js', () => ({
  getIO: jest.fn(() => ({
    emit: mockEmit,
  })),
}));

describe('OrderManager', () => {
  beforeEach(() => {
    tradeQueue.add.mockClear();
    getIO().emit.mockClear();
  });

  it('should create a new order and add it to the queue', async () => {
    const orderDetails = {
      symbol: 'BTC/USD',
      type: OrderType.LIMIT,
      side: OrderSide.BUY,
      amount: 1,
      price: 50000,
    };
    const order = await orderManager.createOrder(orderDetails);
    expect(order.symbol).toBe('BTC/USD');
    expect(order.type).toBe(OrderType.LIMIT);
    expect(order.side).toBe(OrderSide.BUY);
    expect(order.amount).toBe(1);
    expect(order.price).toBe(50000);
    expect(order.status).toBe(OrderStatus.PENDING);
    expect(tradeQueue.add).toHaveBeenCalledWith(order.toObject());
    expect(getIO().emit).toHaveBeenCalledWith('orderUpdate', order.toObject());
  });
});
