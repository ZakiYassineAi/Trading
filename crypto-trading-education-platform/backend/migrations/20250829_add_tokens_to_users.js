// backend/migrations/20250829_add_tokens_to_users.js
exports.up = async function(knex) {
  const exists = await knex.schema.hasColumn('users', 'tokens');
  if (!exists) {
    await knex.schema.table('users', table => {
      table.text('tokens'); // تخزين JSON كسلسلة نصية
    });
    console.log('✅ Column "tokens" added to "users" table.');
  } else {
    console.log('ℹ️ Column "tokens" already exists. Skipping.');
  }
};

exports.down = async function(knex) {
  const exists = await knex.schema.hasColumn('users', 'tokens');
  if (exists) {
    await knex.schema.table('users', table => {
      table.dropColumn('tokens');
    });
    console.log('🗑️ Column "tokens" removed from "users" table.');
  } else {
    console.log('ℹ️ Column "tokens" does not exist. Nothing to drop.');
  }
};
