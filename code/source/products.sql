CREATE TEMPORARY TABLE products (
  product_id STRING,
  product_name STRING,
  category STRING,
  brand STRING,
  price DECIMAL(6, 2),
  commission_rate DECIMAL(6, 2) ,
  PRIMARY KEY (product_id) NOT ENFORCED
) WITH (
  'connector' = '{{ connector }}',
  'url' = '{{ url }}',
  'table-name' = '{{ table_name }}',
  'username' = '{{ username }}',
  'password' = '{{ password }}',
  'driver' = '{{ driver }}'
);