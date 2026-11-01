const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.json());

app.use(express.static(path.join(__dirname, 'public')));

const orders = [
  { id: 1, customer: 'Gauraansh Gaur',  item: 'Veg Momos',     quantity: 2, price: 60, status: 'delivered' },
  { id: 2, customer: 'Ansh Kukreja',  item: 'Veg Sandwich',    quantity: 1, price: 45, status: 'preparing' },
  { id: 3, customer: 'Natasha', item: 'Cold Coffee',     quantity: 3, price: 50, status: 'preparing' },
  { id: 4, customer: 'Tony Stark',  item: 'Cheese Burger',     quantity: 1, price: 80, status: 'placed' },
];
let nextId = 5;


app.get('/orders', (req, res) => {
  res.status(200).json(orders);
});

app.get('/orders/:id', (req, res) => {
  const id = Number(req.params.id);
  const order = orders.find((o) => o.id === id);
  if (!order) {
    return res.status(404).json({ error: `order ${req.params.id} not found` });
  }
  res.status(200).json(order);
});

app.post('/orders', (req, res) => {
  const { customer, item, quantity, price, status } = req.body || {}; 

  const missing = ['customer', 'item', 'quantity', 'price'].filter(
    (f) => req.body?.[f] === undefined || req.body?.[f] === null || req.body?.[f] === ''
  );
  if (missing.length) {
    return res.status(422).json({ error: `required field(s) missing: ${missing.join(', ')}` });
  }


  const qty = Number(quantity);
  const unitPrice = Number(price);
  if (typeof customer !== 'string' || !customer.trim() || typeof item !== 'string' || !item.trim()) {
    return res.status(422).json({ error: 'customer and item must be non-empty text' });
  }
  if (!Number.isInteger(qty) || qty < 1) {
    return res.status(422).json({ error: 'quantity must be a whole number of at least 1' });
  }
  if (!Number.isFinite(unitPrice) || unitPrice < 0) {
    return res.status(422).json({ error: 'price must be a number, 0 or more' });
  }

  const order = {
    id: nextId++,
    customer: customer.trim(),
    item: item.trim(),
    quantity: qty,
    price: unitPrice,
    status: typeof status === 'string' && status.trim() ? status.trim() : 'placed',
  };
  orders.push(order);
  res.status(201).json(order);
});

app.listen(PORT, () => {
  console.log(`CampusEats Orders API running at http://localhost:${PORT}`);
});
