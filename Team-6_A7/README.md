# Assignment - 7
## CampusEats - Orders service (GraphQL)

### Team ID : 6


- <b>Name</b> : Gauraansh Gaur </br>
  <b>Roll no</b> : 20251651039
</br>

- <b>Name</b> : Shraiyansh Chaware </br>
  <b>Roll no</b> : 20251651085
</br>

- <b>Name</b> : Abhishek Yadav </br>
  <b>Roll no</b> : 20251651007
</br>

- <b>Name</b> : Utkarsh Singh </br>
  <b>Roll no</b> : 20251651099
</br>

- <b>Name</b> : Jatin Mandwani </br>
  <b>Roll no</b> : 20251651048
</br>

<br>
<br>

(Google Drive)
https://drive.google.com/drive/folders/1cwoobB0unkD6MUqVqvgWrz3mDOIoMLj9?usp=sharing

<br>

**How to run:** run `schema.sql` in MySQL, put your password in `db.js`, then `npm install && node server.js` and open `public/index.html` with VS Code Live Server.

## Answers

**1. Which CampusEats service did you pick?**
Orders. Each order has an id, customer, item, quantity, total, status and an optional note.

**2. Name one field a client can skip and one it cannot (why we use the "!" sign).**
`note` is nullable (`note: String`), so a client can leave it out when adding an order and it just comes back as `null`. `customer` is `String!`, so the client must always send it, and the server promises it will never return it as null. The `!` is the contract that tells both sides which fields are guaranteed.

**3. Map it to SQL: which part of your query became the WHERE, and which resolver ran the INSERT?**
In `order(id: ID!)`, the `id` argument becomes `WHERE id = ?` in `SELECT * FROM orders WHERE id = ?`. The `Mutation.addOrder` resolver runs the `INSERT INTO orders (...) VALUES (...)`, then does a SELECT to return the new row.

## Sample query and mutation

```graphql
query { orders { id customer item quantity total status } }

mutation {
  addOrder(input: { customer: "Gauraansh", item: "Paneer Roll", total: 90 }) {
    id customer item total status
  }
}
```

## Files

- `schema.graphql` - type, Query and Mutation
- `schema.sql` - table + seed rows
- `db.js` - MySQL connection pool
- `server.js` - Apollo Server + resolvers
- `public/index.html`, `public/style.css` - the demo page
