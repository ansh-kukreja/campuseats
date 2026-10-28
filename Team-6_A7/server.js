const fs = require('fs');
const path = require('path');
const { ApolloServer } = require('@apollo/server');
const { startStandaloneServer } = require('@apollo/server/standalone');
const pool = require('./db');

const typeDefs = fs.readFileSync(path.join(__dirname, 'schema.graphql'), 'utf8');

const resolvers = {
  Query: {
    orders: async () => {
      const [rows] = await pool.query('SELECT * FROM orders ORDER BY id DESC');
      return rows;
    },
    order: async (_parent, { id }) => {
      const [rows] = await pool.query('SELECT * FROM orders WHERE id = ?', [id]);
      return rows[0];
    },
  },

  Mutation: {
    addOrder: async (_parent, { input }) => {
      const { customer, item, quantity, total, note } = input;
      const [result] = await pool.query(
        'INSERT INTO orders (customer, item, quantity, total, note) VALUES (?, ?, ?, ?, ?)',
        [customer, item, quantity, total, note || null]
      );
      const [rows] = await pool.query('SELECT * FROM orders WHERE id = ?', [result.insertId]);
      return rows[0];
    },
  },
};

async function start() {
  const server = new ApolloServer({ typeDefs, resolvers });
  const { url } = await startStandaloneServer(server, { listen: { port: 4000 } });
  console.log(`CampusEats Orders API ready at ${url}`);
}

start();
