exports.up = function(knex) {
  return knex.schema.createTable('news_articles', function(table) {
    table.increments('id').primary();
    table.string('title').notNullable();
    table.string('source');
    table.text('url');
    table.text('summary');
    table.timestamp('published_at').notNullable();
  });
};

exports.down = function(knex) {
  return knex.schema.dropTable('news_articles');
};
