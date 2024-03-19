CREATE TEMPORARY TABLE users (
  user_id STRING,
  name STRING,
  email STRING,
  gender STRING,
  birth_day DATE,
  location STRING,
  phone STRING,
  registration_date DATE,
  PRIMARY KEY (user_id) NOT ENFORCED
) WITH (
  'connector' = '{{ connector }}',
  'url' = '{{ url }}',
  'table-name' = '{{ table_name }}',
  'username' = '{{ username }}',
  'password' = '{{ password }}',
  'driver' = '{{ driver }}'
);