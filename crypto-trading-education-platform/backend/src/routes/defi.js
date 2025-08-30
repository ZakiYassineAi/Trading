import express from 'express';
import { knex } from '../models/database.js';
import { authenticateToken } from './auth.js';

const router = express.Router();

// Get all DeFi simulations for a user
router.get('/simulations', authenticateToken, async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;
    const offset = (page - 1) * limit;

    const query = knex('defi_simulations').where({ user_id: req.user.userId });

    const simulations = await query.clone().orderBy('created_at', 'desc').limit(limit).offset(offset);

    const totalCountResult = await query.clone().count({ count: '*' }).first();
    const totalCount = parseInt(totalCountResult.count, 10);


    // calculate derived properties
    const formattedSimulations = simulations.map(sim => {
      const daysElapsed = sim.status === 'active' ?
        Math.floor((new Date() - new Date(sim.start_date)) / (1000 * 60 * 60 * 24)) :
        sim.duration_days;

      const actualDays = Math.min(daysElapsed, sim.duration_days);
      const earnedReturns = actualDays > 0 ?
        (sim.amount * (sim.simulated_apy / 100) * (actualDays / 365)) : 0;

      return {
        ...sim,
        days_elapsed: actualDays,
        current_value: sim.amount + earnedReturns,
        earned_returns: earnedReturns,
        progress_percentage: (actualDays / sim.duration_days) * 100
      };
    });

    res.json({
      simulations: formattedSimulations,
      pagination: {
        currentPage: parseInt(page),
        totalPages: Math.ceil(totalCount / limit),
        totalCount: totalCount,
        limit: parseInt(limit)
      }
    });
  } catch (error) {
    console.error('Error fetching DeFi simulations:', error);
    res.status(500).json({ error: 'Failed to fetch DeFi simulations.' });
  }
});

// Create a new DeFi simulation
router.post('/simulations', authenticateToken, async (req, res) => {
  try {
    const {
      protocolName,
      simulationType,
      tokenSymbol,
      amount,
      simulatedApy,
      durationDays
    } = req.body;

    if (!protocolName || !simulationType || !tokenSymbol || !amount || !simulatedApy || !durationDays) {
      return res.status(400).json({ error: 'All required fields must be provided.' });
    }

    const validTypes = ['staking', 'yield_farming', 'liquidity_pool'];
    if (!validTypes.includes(simulationType)) {
      return res.status(400).json({ error: 'Invalid simulation type.' });
    }

    if (amount <= 0 || amount > 1000000) {
      return res.status(400).json({ error: 'Amount must be between 0 and 1,000,000.' });
    }

    if (simulatedApy <= 0 || simulatedApy > 1000) {
      return res.status(400).json({ error: 'APY must be between 0% and 1000%.' });
    }

    const startDate = new Date().toISOString().split('T')[0];
    const endDate = new Date(Date.now() + (durationDays * 24 * 60 * 60 * 1000)).toISOString().split('T')[0];
    const projectedReturns = amount * (simulatedApy / 100) * (durationDays / 365);

    const [newSimIdObj] = await knex('defi_simulations').insert({
      user_id: req.user.userId,
      protocol_name: protocolName,
      simulation_type: simulationType,
      token_symbol: tokenSymbol.toUpperCase(),
      amount,
      simulated_apy: simulatedApy,
      duration_days: durationDays,
      projected_returns: projectedReturns,
      start_date: startDate,
      end_date: endDate
    }).returning('id');

    const newSimId = newSimIdObj.id || newSimIdObj;

    const simulation = await knex('defi_simulations').where({ id: newSimId }).first();

    res.status(201).json({
      message: 'DeFi simulation created successfully.',
      simulation: {
        ...simulation,
        current_value: simulation.amount,
        earned_returns: 0,
        progress_percentage: 0,
        educationalOnly: true
      }
    });
  } catch (error) {
    console.error('Error creating DeFi simulation:', error);
    res.status(500).json({ error: 'Failed to create DeFi simulation.' });
  }
});

// Update a DeFi simulation
router.put('/simulations/:id', authenticateToken, async (req, res) => {
  try {
    const simulationId = req.params.id;
    const { simulatedApy, durationDays, status } = req.body;

    const simulation = await knex('defi_simulations')
      .where({ id: simulationId, user_id: req.user.userId })
      .first();

    if (!simulation) {
      return res.status(404).json({ error: 'Simulation not found.' });
    }

    // Recalculate projected returns if APY or duration changes
    const newApy = simulatedApy || simulation.simulated_apy;
    const newDuration = durationDays || simulation.duration_days;
    const projectedReturns = simulation.amount * (newApy / 100) * (newDuration / 365);

    await knex('defi_simulations')
      .where({ id: simulationId })
      .update({
        simulated_apy: newApy,
        duration_days: newDuration,
        projected_returns: projectedReturns,
        status: status || simulation.status,
      });

    const updatedSimulation = await knex('defi_simulations').where({ id: simulationId }).first();

    res.json({
      message: 'Simulation updated successfully.',
      simulation: updatedSimulation
    });
  } catch (error) {
    console.error('Error updating DeFi simulation:', error);
    res.status(500).json({ error: 'Failed to update simulation.' });
  }
});

// Delete a DeFi simulation
router.delete('/simulations/:id', authenticateToken, async (req, res) => {
  try {
    const simulationId = req.params.id;

    const simulation = await knex('defi_simulations')
      .where({ id: simulationId, user_id: req.user.userId })
      .first();

    if (!simulation) {
      return res.status(404).json({ error: 'Simulation not found.' });
    }

    await knex('defi_simulations').where({ id: simulationId }).del();

    res.json({ message: 'Simulation deleted successfully.' });
  } catch (error) {
    console.error('Error deleting DeFi simulation:', error);
    res.status(500).json({ error: 'Failed to delete simulation.' });
  }
});

// Get common DeFi protocol templates
router.get('/protocols', (req, res) => {
  const protocols = [
    {
      name: 'Ethereum 2.0 Staking',
      type: 'staking',
      typical_apy: 4.5,
      risk_level: 'low',
      description: 'Staking on Ethereum 2.0 - low risk and stable returns.'
    },
    {
      name: 'Uniswap Liquidity Pool',
      type: 'liquidity_pool',
      typical_apy: 12.0,
      risk_level: 'medium',
      description: 'Providing liquidity on Uniswap - high returns with medium risk.'
    },
    {
      name: 'PancakeSwap Farming',
      type: 'yield_farming',
      typical_apy: 25.0,
      risk_level: 'high',
      description: 'Yield farming on PancakeSwap - very high returns with high risk.'
    },
    {
      name: 'Compound Lending',
      type: 'yield_farming',
      typical_apy: 6.8,
      risk_level: 'medium',
      description: 'Lending on Compound - moderate returns with limited risk.'
    },
    {
      name: 'Curve Finance Pool',
      type: 'liquidity_pool',
      typical_apy: 8.5,
      risk_level: 'low',
      description: 'Curve Finance liquidity - low risk and moderate returns.'
    },
    {
      name: 'Cardano Staking',
      type: 'staking',
      typical_apy: 5.2,
      risk_level: 'low',
      description: 'Staking Cardano - safe and reliable.'
    },
    {
      name: 'Solana Staking',
      type: 'staking',
      typical_apy: 7.3,
      risk_level: 'medium',
      description: 'Staking Solana - good returns with moderate risk.'
    },
    {
      name: 'Avalanche Validator',
      type: 'staking',
      typical_apy: 9.1,
      risk_level: 'medium',
      description: 'Running an Avalanche validator node - high returns.'
    }
  ];

  res.json({ protocols });
});

// DeFi yield calculator
router.post('/calculator', (req, res) => {
  try {
    const { amount, apy, durationDays, compoundFrequency = 365 } = req.body;

    if (!amount || !apy || !durationDays) {
      return res.status(400).json({
        error: 'Amount, APY, and duration are required.'
      });
    }

    const principal = parseFloat(amount);
    const annualRate = parseFloat(apy) / 100;
    const days = parseInt(durationDays);
    const compound = parseInt(compoundFrequency);

    // Simple interest
    const simpleReturn = principal * annualRate * (days / 365);
    const simpleTotal = principal + simpleReturn;

    // Compound interest
    const compoundTotal = principal * Math.pow(
      (1 + annualRate / compound),
      (compound * days / 365)
    );
    const compoundReturn = compoundTotal - principal;

    // Average returns
    const dailyReturn = (compoundTotal / principal - 1) / days;
    const monthlyReturn = dailyReturn * 30;
    const weeklyReturn = dailyReturn * 7;

    res.json({
      input: {
        amount: principal,
        apy: parseFloat(apy),
        duration_days: days,
        compound_frequency: compound
      },
      results: {
        simple_interest: {
          total: Math.round(simpleTotal * 100) / 100,
          return: Math.round(simpleReturn * 100) / 100
        },
        compound_interest: {
          total: Math.round(compoundTotal * 100) / 100,
          return: Math.round(compoundReturn * 100) / 100
        },
        breakdown: {
          daily_return_percent: Math.round(dailyReturn * 10000) / 100,
          weekly_return_percent: Math.round(weeklyReturn * 10000) / 100,
          monthly_return_percent: Math.round(monthlyReturn * 10000) / 100
        },
        total_return_percentage: Math.round(((compoundTotal / principal) - 1) * 10000) / 100
      },
      note: 'These are approximate calculations for educational purposes only.'
    });
  } catch (error) {
    console.error('Error in DeFi calculator:', error);
    res.status(500).json({ error: 'Failed to calculate yield.' });
  }
});

export default router;