exports.up = function(knex) {
  return knex.schema.createTable('historical_data', function(table) {
    table.increments('id').primary();
    table.string('symbol').notNullable();
    table.timestamp('timestamp').notNullable();
    table.decimal('open', 18, 8).notNullable();
    table.decimal('high', 18, 8).notNullable();
    table.decimal('low', 18, 8).notNullable();
    table.decimal('close', 18, 8).notNullable();
    table.decimal('volume', 18, 8).notNullable();
  });
};

exports.down = function(knex) {
  return knex.schema.dropTable('historical_data');
};
