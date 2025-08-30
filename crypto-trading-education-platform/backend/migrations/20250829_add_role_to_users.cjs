// backend/migrations/20250829_add_role_to_users.js
exports.up = async function(knex) {
  const exists = await knex.schema.hasColumn('users', 'role');
  if (!exists) {
    await knex.schema.table('users', table => {
      table.string('role').notNullable().defaultTo('user');
    });
    console.log('✅ Column "role" added to "users" table.');
  } else {
    console.log('ℹ️ Column "role" already exists. Skipping.');
  }
};

exports.down = async function(knex) {
  const exists = await knex.schema.hasColumn('users', 'role');
  if (exists) {
    await knex.schema.table('users', table => {
      table.dropColumn('role');
    });
    console.log('🗑️ Column "role" removed from "users" table.');
  } else {
    console.log('ℹ️ Column "role" does not exist. Nothing to drop.');
  }
};
