exports.up = function(knex) {
  return knex.schema.createTable('audit_logs', function(table) {
    table.increments('id').primary();
    table.string('action').notNullable();
    table.string('resource_type');
    table.text('details');
    table.string('severity').defaultTo('info');
    table.string('ip_address');
    table.text('user_agent');
    table.timestamp('timestamp').defaultTo(knex.fn.now());
  });
};

exports.down = function(knex) {
  return knex.schema.dropTable('audit_logs');
};
