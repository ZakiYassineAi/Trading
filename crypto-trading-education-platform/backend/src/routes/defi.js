import express from 'express';
import { db } from '../models/database.js';
import { authenticateToken } from './auth.js';

const router = express.Router();

// الحصول على جميع محاكاة DeFi للمستخدم
router.get('/simulations', authenticateToken, async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;
    const offset = (page - 1) * limit;

    const simulations = await db.all(`
      SELECT * FROM defi_simulations WHERE user_id = ?
      ORDER BY created_at DESC
      LIMIT ? OFFSET ?
    `, [req.user.userId, limit, offset]);

    const totalCount = await db.get(`
      SELECT COUNT(*) as count FROM defi_simulations WHERE user_id = ?
    `, [req.user.userId]);

    // حساب العوائد المتوقعة للمحاكاة النشطة
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
        totalPages: Math.ceil(totalCount.count / limit),
        totalCount: totalCount.count,
        limit: parseInt(limit)
      }
    });
  } catch (error) {
    throw error;
  }
});

// إنشاء محاكاة DeFi جديدة
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
      return res.status(400).json({
        error: 'يجب إدخال جميع البيانات المطلوبة'
      });
    }

    const validTypes = ['staking', 'yield_farming', 'liquidity_pool'];
    if (!validTypes.includes(simulationType)) {
      return res.status(400).json({
        error: 'نوع المحاكاة غير صالح'
      });
    }

    if (amount <= 0 || amount > 1000000) {
      return res.status(400).json({
        error: 'المبلغ يجب أن يكون بين 0 و 1,000,000'
      });
    }

    if (simulatedApy <= 0 || simulatedApy > 1000) {
      return res.status(400).json({
        error: 'معدل العائد يجب أن يكون بين 0% و1000%'
      });
    }

    const startDate = new Date().toISOString().split('T')[0];
    const endDate = new Date(Date.now() + (durationDays * 24 * 60 * 60 * 1000)).toISOString().split('T')[0];
    const projectedReturns = amount * (simulatedApy / 100) * (durationDays / 365);

    const result = await db.run(`
      INSERT INTO defi_simulations (
        user_id, protocol_name, simulation_type, token_symbol, amount,
        simulated_apy, duration_days, projected_returns, start_date, end_date
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `, [
      req.user.userId, protocolName, simulationType, tokenSymbol.toUpperCase(),
      amount, simulatedApy, durationDays, projectedReturns, startDate, endDate
    ]);

    const simulation = await db.get(`
      SELECT * FROM defi_simulations WHERE id = ?
    `, [result.lastID]);

    res.status(201).json({
      message: 'تم إنشاء محاكاة DeFi بنجاح',
      simulation: {
        ...simulation,
        current_value: simulation.amount,
        earned_returns: 0,
        progress_percentage: 0,
        educationalOnly: true
      }
    });
  } catch (error) {
    throw error;
  }
});

// تحديث محاكاة DeFi
router.put('/simulations/:id', authenticateToken, async (req, res) => {
  try {
    const simulationId = req.params.id;
    const { simulatedApy, durationDays, status } = req.body;

    const simulation = await db.get(`
      SELECT * FROM defi_simulations WHERE id = ? AND user_id = ?
    `, [simulationId, req.user.userId]);

    if (!simulation) {
      return res.status(404).json({
        error: 'المحاكاة غير موجودة'
      });
    }

    // حساب العوائد المتوقعة الجديدة إذا تغيرت
    const newApy = simulatedApy || simulation.simulated_apy;
    const newDuration = durationDays || simulation.duration_days;
    const newProjectedReturns = simulation.amount * (newApy / 100) * (newDuration / 365);

    await db.run(`
      UPDATE defi_simulations
      SET simulated_apy = ?, duration_days = ?, projected_returns = ?, status = ?
      WHERE id = ?
    `, [
      newApy,
      newDuration,
      newProjectedReturns,
      status || simulation.status,
      simulationId
    ]);

    const updatedSimulation = await db.get(`
      SELECT * FROM defi_simulations WHERE id = ?
    `, [simulationId]);

    res.json({
      message: 'تم تحديث المحاكاة بنجاح',
      simulation: updatedSimulation
    });
  } catch (error) {
    throw error;
  }
});

// حذف محاكاة DeFi
router.delete('/simulations/:id', authenticateToken, async (req, res) => {
  try {
    const simulationId = req.params.id;

    const simulation = await db.get(`
      SELECT * FROM defi_simulations WHERE id = ? AND user_id = ?
    `, [simulationId, req.user.userId]);

    if (!simulation) {
      return res.status(404).json({
        error: 'المحاكاة غير موجودة'
      });
    }

    await db.run(`DELETE FROM defi_simulations WHERE id = ?`, [simulationId]);

    res.json({ message: 'تم حذف المحاكاة بنجاح' });
  } catch (error) {
    throw error;
  }
});

// الحصول على قوالب بروتوكولات DeFi الشائعة
router.get('/protocols', (req, res) => {
  const protocols = [
    {
      name: 'Ethereum 2.0 Staking',
      type: 'staking',
      typical_apy: 4.5,
      risk_level: 'low',
      description: 'ستاكينغ إيثيريوم 2.0 - مخاطر منخفضة وعوائد مستقرة'
    },
    {
      name: 'Uniswap Liquidity Pool',
      type: 'liquidity_pool',
      typical_apy: 12.0,
      risk_level: 'medium',
      description: 'توفير السيولة في Uniswap - عوائد عالية مع مخاطر متوسطة'
    },
    {
      name: 'PancakeSwap Farming',
      type: 'yield_farming',
      typical_apy: 25.0,
      risk_level: 'high',
      description: 'زراعة العوائد في PancakeSwap - عوائد عالية جداً مع مخاطر عالية'
    },
    {
      name: 'Compound Lending',
      type: 'yield_farming',
      typical_apy: 6.8,
      risk_level: 'medium',
      description: 'إقراض في Compound - عوائد معتدلة مع مخاطر محدودة'
    },
    {
      name: 'Curve Finance Pool',
      type: 'liquidity_pool',
      typical_apy: 8.5,
      risk_level: 'low',
      description: 'سيولة Curve Finance - منخفضة المخاطر وعوائد معتدلة'
    },
    {
      name: 'Cardano Staking',
      type: 'staking',
      typical_apy: 5.2,
      risk_level: 'low',
      description: 'ستاكينغ كاردانو - آمن ومعتمد'
    },
    {
      name: 'Solana Staking',
      type: 'staking',
      typical_apy: 7.3,
      risk_level: 'medium',
      description: 'ستاكينغ سولانا - عوائد جيدة مع مخاطر معتدلة'
    },
    {
      name: 'Avalanche Validator',
      type: 'staking',
      typical_apy: 9.1,
      risk_level: 'medium',
      description: 'تشغيل عقدة Avalanche - عوائد مرتفعة'
    }
  ];

  res.json({ protocols });
});

// حاسبة عوائد DeFi
router.post('/calculator', (req, res) => {
  try {
    const { amount, apy, durationDays, compoundFrequency = 365 } = req.body;

    if (!amount || !apy || !durationDays) {
      return res.status(400).json({
        error: 'يجب إدخال المبلغ ومعدل العائد والمدة'
      });
    }

    const principal = parseFloat(amount);
    const annualRate = parseFloat(apy) / 100;
    const days = parseInt(durationDays);
    const compound = parseInt(compoundFrequency);

    // عوائد بسيطة
    const simpleReturn = principal * annualRate * (days / 365);
    const simpleTotal = principal + simpleReturn;

    // عوائد مركبة
    const compoundTotal = principal * Math.pow(
      (1 + annualRate / compound),
      (compound * days / 365)
    );
    const compoundReturn = compoundTotal - principal;

    // حساب متوسط العوائد اليومية
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
          daily_return: Math.round(dailyReturn * 10000) / 100, // نسبة مئوية
          weekly_return: Math.round(weeklyReturn * 10000) / 100,
          monthly_return: Math.round(monthlyReturn * 10000) / 100
        },
        total_return_percentage: Math.round(((compoundTotal / principal) - 1) * 10000) / 100
      },
      note: 'هذه حسابات تقريبية لأغراض تعليمية فقط'
    });
  } catch (error) {
    throw error;
  }
});

export default router;