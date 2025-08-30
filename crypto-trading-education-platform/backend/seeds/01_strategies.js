/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.seed = async function(knex) {
  // Deletes ALL existing entries
  await knex('strategies').del()

  // Inserts seed entries
  await knex('strategies').insert([
    {
      name: 'Simple Moving Average (SMA) Crossover',
      description: 'A basic strategy that generates signals when a short-term SMA crosses a long-term SMA.',
      parameters: JSON.stringify({ short_window: 50, long_window: 200 })
    },
    {
      name: 'Relative Strength Index (RSI)',
      description: 'A momentum oscillator that measures the speed and change of price movements. Buys when oversold, sells when overbought.',
      parameters: JSON.stringify({ rsi_period: 14, overbought_level: 70, oversold_level: 30 })
    },
    {
      name: 'MACD Strategy',
      description: 'Uses the Moving Average Convergence Divergence (MACD) indicator to identify trend changes.',
      parameters: JSON.stringify({ fast_period: 12, slow_period: 26, signal_period: 9 })
    }
  ]);
};
