CREATE SCHEMA shop;

SET search_path TO shop;

CREATE TABLE users (
  user_id VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255),
  gender VARCHAR(2),
  birth_day DATE,
  location VARCHAR(255),
  phone VARCHAR(255),
  registration_date DATE 
);

CREATE TABLE products (
  product_id VARCHAR(355) PRIMARY KEY,
  product_name VARCHAR(355),
  category VARCHAR(355),
  brand VARCHAR(355),
  price DECIMAL,
  commission_rate DECIMAL
);

-- Copy users data from CSV into users table
COPY users (user_id, name, email, gender, birth_day, location, phone, registration_date)
FROM '/postgres/data/Users.csv'
DELIMITER ',' CSV HEADER;

-- Copy products data from CSV into products table
COPY products (product_id, product_name, category, brand, price, commission_rate)
FROM '/postgres/data/Products.csv'
DELIMITER ',' CSV HEADER;

CREATE TABLE checkout_attribution (
  checkout_id VARCHAR(255) PRIMARY KEY,
  user_id VARCHAR(255),
  product_id VARCHAR(255),
  quantity INT,
  total_amount DOUBLE PRECISION,
  payment_method VARCHAR(255),
  payment_status VARCHAR(255),
  payment_description VARCHAR(255),
  gender VARCHAR(255),
  category VARCHAR(255),
  profit DOUBLE PRECISION,
  source VARCHAR(255),
  checkout_timestamp TIMESTAMP,
  click_timestamp TIMESTAMP
);

-- Create a role for Grafana to access the database
CREATE ROLE grafana WITH LOGIN PASSWORD 'grafana';
GRANT USAGE ON SCHEMA shop TO grafana;
GRANT SELECT ON TABLE shop.checkout_attribution TO grafana;
ALTER ROLE grafana SET search_path = 'shop';