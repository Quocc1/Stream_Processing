from dataclasses import dataclass, field, asdict
from typing import List

from jinja2 import Environment, FileSystemLoader
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

# Jar files to read data from kafka and connect to postgresql
REQUIRED_JAR = [
  "file:///opt/flink/flink-sql-connector-kafka-3.0.2-1.18.jar",
  "file:///opt/flink/flink-connector-jdbc-3.1.1-1.17.jar",
  "file:///opt/flink/postgresql-42.7.1.jar",
]

# Configuration
@dataclass(frozen=True)
class FlinkJobConfig:
  job_name: str = 'checkout_attribution_job'
  jars: List[str] = field(default_factory=lambda: REQUIRED_JAR)
  checkpoint_interval: int = 10
  checkpoint_pause: int = 5
  checkpoint_timeout: int = 5
  parallelism: int = 2
  
@dataclass(frozen=True)
class KafkaConfig:
  connector:str = 'kafka'
  bootstrap_servers: str = 'kafka:9092'
  scan_startup_mode: str = 'earliest-offset'
  group_id: str = 'flink-consumer'

@dataclass(frozen=True)
class ClickTopicConfig(KafkaConfig):
  topic: str = 'clicks'
  format: str = 'json'

@dataclass(frozen=True)
class CheckoutTopicConfig(KafkaConfig):
  topic: str = 'checkouts'
  format: str = 'json'
  
@dataclass(frozen=True)
class PostgresConfig:
  connector: str = 'jdbc'
  driver: str = 'org.postgresql.Driver'
  url: str = 'jdbc:postgresql://postgres:5432/postgres'
  username: str = 'postgres'
  password: str = 'postgres'

@dataclass(frozen=True)
class UserTableConfig(PostgresConfig):
  table_name: str = 'shop.users'

@dataclass(frozen=True)
class ProductTableConfig(PostgresConfig):
  table_name: str = 'shop.products'

@dataclass(frozen=True)
class CheckoutAttributionTableConfig(PostgresConfig):
  table_name: str = 'shop.checkout_attribution'
  
# Get executuion environment for Flink
def get_execution_environment(config: FlinkJobConfig) -> StreamTableEnvironment:
  stream_env = StreamExecutionEnvironment.get_execution_environment()
  for jar in config.jars:
    stream_env.add_jars(jar)
    
  # Start a checkpoint for every 10 seconds
  stream_env.enable_checkpointing(config.checkpoint_interval * 1000)
  
  # Ensure there is 5 seconds of progress happen between each checkpoint
  stream_env.get_checkpoint_config().set_min_pause_between_checkpoints(config.checkpoint_pause)
  
  # Discard checkpoint if it not completed in 5 minutes
  stream_env.get_checkpoint_config().set_checkpoint_timeout(config.checkpoint_timeout * 1000 * 60)
  
  # Set parallelism
  execute_config = stream_env.get_config()
  execute_config.set_parallelism(config.parallelism)
  
  table_env = StreamTableEnvironment.create(stream_env)
  job_config = table_env.get_config().get_configuration()
  job_config.set_string('pipeline.name', config.job_name)
  
  return table_env
    
def get_sql_query(
  entity: str, 
  type: str, 
  template_env: Environment = Environment(loader=FileSystemLoader('code/'))
) -> str:
  config_map = {
    'clicks': ClickTopicConfig(),
    'checkouts': CheckoutTopicConfig(),
    'users': UserTableConfig(),
    'products': ProductTableConfig(),
    'checkout_attribution': CheckoutAttributionTableConfig(),
    'insert_into_sink': CheckoutAttributionTableConfig()
  }
  
  return template_env.get_template(f'{type}/{entity}.sql').render(
    asdict(config_map.get(entity))
  )
  
def run_checkout_attribution_job(table_env: StreamTableEnvironment, get_sql_query=get_sql_query) -> None:
  # Create the source table
  table_env.execute_sql(get_sql_query('clicks', 'source'))
  table_env.execute_sql(get_sql_query('checkouts', 'source'))
  table_env.execute_sql(get_sql_query('users', 'source'))
  table_env.execute_sql(get_sql_query('products', 'source'))
  
  # Create the sink table
  table_env.execute_sql(get_sql_query('checkout_attribution', 'sink'))
  
  # Run processing query
  statement_set = table_env.create_statement_set()
  statement_set.add_insert_sql(get_sql_query('insert_into_sink', 'process'))
  checkout_attribution_job = statement_set.execute()
  print(
    f"""
    Running checkout attribution job:
    Status: {checkout_attribution_job.get_job_client().get_job_status()}
    """
  )
  
if __name__ == "__main__":
  table_env = get_execution_environment(FlinkJobConfig())
  run_checkout_attribution_job(table_env)