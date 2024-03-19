CREATE TABLE clicks (
  click_id STRING,
  user_id STRING,
  source STRING,
  user_agent STRING,
  ip_address STRING,
  click_timestamp TIMESTAMP(3),
  processing_timestamp as PROCTIME(),
  WATERMARK FOR click_timestamp AS click_timestamp - INTERVAL '15' SECOND
) WITH (
  'connector' = '{{ connector }}',
  'topic' =  '{{ topic }}',
  'properties.bootstrap.servers' = '{{ bootstrap_servers }}',
  'properties.group.id' = '{{ group_id }}',
  'format' = '{{ format }}',
  'scan.startup.mode' = '{{ scan_startup_mode }}'
);