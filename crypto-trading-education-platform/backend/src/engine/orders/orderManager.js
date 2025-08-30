import Order from './Order.js';
import { tradeQueue } from '../queue.js';
import { getIO } from '../websockets/socketServer.js';

class OrderManager {
  constructor() {
    this.activeOrders = new Map();
    this._setupQueueProcessor();
  }

  async createOrder(orderDetails) {
    const order = new Order(orderDetails);
    this.activeOrders.set(order.id, order);

    // Add order to the high-priority trading queue
    await tradeQueue.add(order.toObject());
    console.log(`[OrderManager] Order ${order.id} for ${order.symbol} added to the queue.`);

    // Emit event to notify clients
    getIO().emit('orderUpdate', order.toObject());

    return order;
  }

  cancelOrder(orderId) {
    const order = this.activeOrders.get(orderId);
    if (order) {
      // Logic to cancel an order will be more complex, involving communication
      // with the exchange. For now, we'll just update the status.
      order.updateStatus('CANCELED');
      getIO().emit('orderUpdate', order.toObject());
      this.activeOrders.delete(orderId);
      console.log(`[OrderManager] Order ${orderId} has been canceled.`);
      return true;
    }
    return false;
  }

  _setupQueueProcessor() {
    tradeQueue.process(async (job) => {
      const orderData = job.data;
      console.log(`[QueueProcessor] Processing order ${orderData.id}...`);
      // In a real system, this is where the order would be sent
      // to the exchange via the smart order router.
      // For now, we'll just simulate a fill.
      setTimeout(() => {
        const order = this.activeOrders.get(orderData.id);
        if (order) {
          order.updateStatus('FILLED');
          getIO().emit('orderUpdate', order.toObject());
          console.log(`[QueueProcessor] Order ${orderData.id} has been filled (simulated).`);
          this.activeOrders.delete(orderData.id);
        }
      }, 2000); // Simulate 2-second execution time
    });
  }
}

// Export a singleton instance
const orderManager = new OrderManager();
export default orderManager;
