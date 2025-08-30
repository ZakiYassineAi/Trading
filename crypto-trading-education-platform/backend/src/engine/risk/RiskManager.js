class RiskManager {
  constructor() {
    // 5% of portfolio
    this.max_position_size = 0.05;
    // 2% daily loss limit
    this.max_daily_loss = 0.02;
    // Asset correlation tracking
    this.correlation_matrix = {};
  }

  /**
   * Checks if a proposed trade is compliant with risk rules.
   * @param {object} trade - The trade object { symbol, side, amount, price }.
   * @param {object} portfolio - The current portfolio state.
   * @returns {boolean} - True if the trade is allowed, false otherwise.
   */
  validate(trade, portfolio) {
    console.log(`[RiskManager] Validating trade for ${trade.symbol}...`);
    // Stub implementation: Always approve for now.
    // Real implementation would check position size, daily loss, etc.
    if ((trade.amount * trade.price) / portfolio.totalValue > this.max_position_size) {
      console.warn(`[RiskManager] Trade rejected: Exceeds max position size.`);
      return false;
    }

    console.log(`[RiskManager] Trade for ${trade.symbol} approved.`);
    return true;
  }
}

// Export a singleton instance
const riskManager = new RiskManager();
export default riskManager;
