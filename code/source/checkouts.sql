CREATE TABLE checkouts (
  checkout_id STRING,
  user_id STRING,
  product_id STRING,
  quantity INT,
  shipping_cost DECIMAL(6, 2),
  discount DECIMAL(6, 2),
  payment_method STRING,
  payment_status STRING,
  payment_description STRING,
  shipping_address STRING,
  checkout_timestamp TIMESTAMP(3),
  processing_timestamp AS PROCTIME(),
  WATERMARK FOR checkout_timestamp AS checkout_timestamp - INTERVAL '15' SECOND
) WITH (
  'connector' = '{{ connector }}',
  'topic' =  '{{ topic }}',
  'properties.bootstrap.servers' = '{{ bootstrap_servers }}',
  'properties.group.id' = '{{ group_id }}',
  'format' = '{{ format }}',
  'scan.startup.mode' = '{{ scan_startup_mode }}'
);