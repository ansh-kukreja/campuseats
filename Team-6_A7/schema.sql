CREATE DATABASE IF NOT EXISTS campuseats;
USE campuseats;

CREATE TABLE orders (
  id       INT AUTO_INCREMENT PRIMARY KEY,
  customer VARCHAR(100) NOT NULL,
  item     VARCHAR(100) NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  total    DECIMAL(8,2) NOT NULL,
  status   VARCHAR(20) NOT NULL DEFAULT 'PLACED',
  note     VARCHAR(200)
);

INSERT INTO orders (customer, item, quantity, total, status, note) VALUES
  ('Aarav Shah',  'Veg Burger',   2, 180.00, 'DELIVERED', NULL),
  ('Meera Nair',  'Masala Dosa',  1,  70.00, 'PREPARING', 'less spicy please'),
  ('Kabir Singh', 'Cold Coffee',  3, 210.00, 'PLACED',    NULL),
  ('Isha Verma',  'Paneer Roll',  2, 180.00, 'PLACED',    'extra mayo');
