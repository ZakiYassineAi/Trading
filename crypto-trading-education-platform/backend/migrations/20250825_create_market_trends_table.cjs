exports.up = function(knex) {
  return knex.schema.createTable('market_trends', function(table) {
    table.increments('id').primary();
    table.string('trend_name').notNullable();
    table.text('description');
    table.json('indicator_data');
    table.timestamp('timestamp').defaultTo(knex.fn.now());
  });
};

exports.down = function(knex) {
  return knex.schema.dropTable('market_trends');
};
