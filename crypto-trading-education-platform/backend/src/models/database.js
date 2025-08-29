// backend/src/models/database.js
const knexConfig = require('../../knexfile');
const env = process.env.NODE_ENV || 'development';
const knex = require('knex')(knexConfig[env]);

// واجهة التعامل مع قاعدة البيانات
module.exports = {
  knex,

  // جلب جميع المستخدمين
  getUsers: () => knex('users').select('*'),

  // جلب مستخدم واحد
  getUserById: (id) => knex('users').where({ id }).first(),

  // حفظ التوكنز لمستخدم
  saveTokens: async (userId, tokenObj) => {
    const tokensJson = JSON.stringify(tokenObj);
    return knex('users').where({ id: userId }).update({ tokens: tokensJson });
  },

  // جلب التوكنز لمستخدم
  getTokens: async (userId) => {
    const row = await knex('users').where({ id: userId }).first('tokens');
    return row && row.tokens ? JSON.parse(row.tokens) : null;
  }
};
