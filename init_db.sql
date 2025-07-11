DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT,
    signup_date DATE
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    price REAL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    payment_date DATE,
    amount REAL,
    method TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

INSERT INTO customers (id, name, country, signup_date) VALUES
 (1,'Alice','USA','2024-01-05'),
 (2,'Bob','UK','2024-03-10'),
 (3,'Choi','KR','2024-06-22'),
 (4,'Dara','ID','2025-01-15');

INSERT INTO products (id, name, category, price) VALUES
 (1,'Laptop Pro','Electronics',1500.00),
 (2,'Noise-Canceling Headphones','Electronics',300.00),
 (3,'Standing Desk','Furniture',450.00),
 (4,'Ergonomic Chair','Furniture',250.00),
 (5,'Monitor 27"','Electronics',350.00);

INSERT INTO orders (id, customer_id, order_date, total) VALUES
 (1,1,'2025-02-01',1850.00),
 (2,2,'2025-02-03',600.00),
 (3,3,'2025-02-05',350.00),
 (4,1,'2025-02-07',450.00);

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
 (1,1,1,1500.00),
 (1,2,1,300.00),
 (1,5,1,350.00),
 (2,3,1,450.00),
 (2,4,1,250.00),
 (3,5,1,350.00),
 (4,3,1,450.00);

INSERT INTO payments (id, order_id, payment_date, amount, method) VALUES
 (1,1,'2025-02-01',1850.00,'Credit Card'),
 (2,2,'2025-02-03',600.00,'PayPal'),
 (3,3,'2025-02-05',350.00,'Credit Card'),
 (4,4,'2025-02-07',450.00,'Bank Transfer');
