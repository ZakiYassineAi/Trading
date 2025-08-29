// knexfile.js
module.exports = {
  development: {
    client: 'sqlite3',
    connection: {
      filename: './data/app.db'
    },
    useNullAsDefault: true,
    migrations: {
      directory: './migrations'
    },
    pool: {
      afterCreate: (conn, cb) => conn.run('PRAGMA foreign_keys = ON', cb)
    }
  },

  production: {
    client: 'sqlite3',
    connection: {
      filename: './data/app.db'
    },
    useNullAsDefault: true,
    migrations: {
      directory: './migrations'
    },
    pool: {
      afterCreate: (conn, cb) => conn.run('PRAGMA foreign_keys = ON', cb)
    }
  }
};
