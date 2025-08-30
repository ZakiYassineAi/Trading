export const OrderType = Object.freeze({
  MARKET: 'MARKET',
  LIMIT: 'LIMIT',
  STOP_LOSS: 'STOP_LOSS',
  TAKE_PROFIT: 'TAKE_PROFIT',
  BRACKET: 'BRACKET',
  TRAILING_STOP: 'TRAILING_STOP',
});

export const OrderSide = Object.freeze({
  BUY: 'BUY',
  SELL: 'SELL',
});

export const OrderStatus = Object.freeze({
  PENDING: 'PENDING',
  OPEN: 'OPEN',
  FILLED: 'FILLED',
  CANCELED: 'CANCELED',
  REJECTED: 'REJECTED',
});
