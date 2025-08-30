import express from 'express';
import { knex } from '../models/database.js';
import { authenticateToken } from './auth.js';

const router = express.Router();

// Get all alerts
router.get('/', authenticateToken, async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;
    const offset = (page - 1) * limit;

    const query = knex('alerts').where({ user_id: req.user.id });

    const alerts = await query.clone().orderBy('created_at', 'desc').limit(limit).offset(offset);

    const totalCountResult = await query.clone().count({ count: '*' }).first();
    const totalCount = parseInt(totalCountResult.count, 10);

    const formattedAlerts = alerts.map(alert => ({
      ...alert,
      notification_methods: JSON.parse(alert.notification_methods || '[]')
    }));

    res.json({
      alerts: formattedAlerts,
      pagination: {
        currentPage: parseInt(page),
        totalPages: Math.ceil(totalCount / limit),
        totalCount: totalCount,
        limit: parseInt(limit)
      }
    });
  } catch (error) {
    console.error('Error fetching alerts:', error);
    res.status(500).json({ error: 'Failed to fetch alerts.' });
  }
});

// Create a new alert
router.post('/', authenticateToken, async (req, res) => {
  try {
    const {
      symbol,
      condition,
      value,
      notes
    } = req.body;

    if (!symbol || !condition || !value) {
      return res.status(400).json({ error: 'Symbol, condition, and value are required.' });
    }

    const [newAlert] = await knex('alerts').insert({
      user_id: req.user.id,
      symbol,
      condition,
      value,
      notes,
    }).returning('*');

    res.status(201).json(newAlert);
  } catch (error) {
    console.error('Error creating alert:', error);
    res.status(500).json({ error: 'Failed to create alert.' });
  }
});

// Delete an alert
router.delete('/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    const deletedCount = await knex('alerts')
      .where({ id, user_id: req.user.id })
      .del();

    if (deletedCount === 0) {
      return res.status(404).json({ error: 'Alert not found or you do not have permission to delete it.' });
    }

    res.status(204).send();
  } catch (error) {
    console.error('Error deleting alert:', error);
    res.status(500).json({ error: 'Failed to delete alert.' });
  }
});

export default router;