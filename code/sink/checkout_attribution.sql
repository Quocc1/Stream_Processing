CREATE TABLE checkout_attribution (
  checkout_id STRING,
  user_id STRING,
  product_id STRING,
  quantity INT,
  total_amount DECIMAL(6, 2),
  payment_method STRING,
  payment_status STRING,
  payment_description STRING,
  gender STRING,
  category STRING,
  profit DECIMAL(6, 2),
  source STRING,
  checkout_timestamp TIMESTAMP(3),
  click_timestamp TIMESTAMP,
  PRIMARY KEY (checkout_id) NOT ENFORCED
) WITH (
  'connector' = '{{ connector }}',
  'url' = '{{ url }}',
  'table-name' = '{{ table_name }}',
  'username' = '{{ username }}',
  'password' = '{{ password }}',
  'driver' = '{{ driver }}'
);