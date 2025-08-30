class PortfolioManager {
  constructor() {
    this.positions = new Map(); // { 'BTC-USD': { amount: 1.5, entryPrice: 50000 }, ... }
    this.cash = 100000; // Starting with $100,000
  }

  /**
   * Calculates the total value of the portfolio.
   * @param {object} currentPrices - A map of current prices, e.g., { 'BTC-USD': 52000 }.
   * @returns {number} - The total portfolio value.
   */
  getTotalValue(currentPrices) {
    let totalValue = this.cash;
    for (const [symbol, position] of this.positions.entries()) {
      const currentPrice = currentPrices[symbol] || position.entryPrice;
      totalValue += position.amount * currentPrice;
    }
    return totalValue;
  }

  /**
   * Updates the portfolio after a trade is executed.
   * @param {object} trade - The executed trade object { symbol, side, amount, price }.
   */
  updatePortfolio(trade) {
    console.log(`[PortfolioManager] Updating portfolio for trade: ${trade.side} ${trade.amount} ${trade.symbol}`);
    // This is a stub. A real implementation would be more complex,
    // handling partial fills, fees, etc.
    const existingPosition = this.positions.get(trade.symbol) || { amount: 0, entryPrice: 0 };
    const cost = trade.amount * trade.price;

    if (trade.side === 'BUY') {
      this.cash -= cost;
      const newAmount = existingPosition.amount + trade.amount;
      const newEntryPrice = ((existingPosition.amount * existingPosition.entryPrice) + cost) / newAmount;
      this.positions.set(trade.symbol, { amount: newAmount, entryPrice: newEntryPrice });
    } else { // SELL
      this.cash += cost;
      existingPosition.amount -= trade.amount;
      if (existingPosition.amount <= 0) {
        this.positions.delete(trade.symbol);
      } else {
        this.positions.set(trade.symbol, existingPosition);
      }
    }
  }
}

// Export a singleton instance
const portfolioManager = new PortfolioManager();
export default portfolioManager;
