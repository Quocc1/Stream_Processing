import time
import json
import random
from uuid import uuid4
from typing import Optional
from datetime import datetime

import pandas as pd
from faker import Faker
from confluent_kafka import Producer


fake = Faker()

def get_id_list(type: str) -> list:
    file_path = f'./generate_data/data/{type}.csv'
    df = pd.read_csv(file_path)
    column_name = 'User_id' if type == 'Users' else 'Product_ID'
    id_list = df[column_name].tolist()
    return id_list
    
# Get user id list
def get_user_id_list() -> list:
  return get_id_list('Users')

# Get product id list
def get_product_id_list() -> list:
  return get_id_list('Products')

# Get a random user id
def get_random_user_id() -> str:
  random_index = random.randint(0, len(get_user_id_list()) - 1)
  return get_user_id_list()[random_index]

# Get a random product id
def get_random_product_id() -> str:
  random_index = random.randint(0, len(get_product_id_list()) - 1)
  return get_product_id_list()[random_index]

# Create a random user agent
def generate_user_agent() -> str:
  return fake.user_agent()


# Create a random IP address:
def generate_ip_address() -> str:
  return fake.ipv4()

# Push event to kafka topic
def push_to_kafka(event: dict, topic: str) -> None:
  producer = Producer({'bootstrap.servers': 'kafka:9092'})
  producer.produce(topic=topic, value=json.dumps(event).encode('utf-8'))
  producer.flush()


# Generate click event with the current event_timestamp
def generate_click_event(user_id: Optional[str] = None) -> dict:
  click_id = str(uuid4())
  user_id = user_id if user_id else get_random_user_id()
  source  = random.choice(["Unknown", "Facebook", "Unknown", "Twitter", "Tiktok", "Gmail", "Unknown", 
                            "Google", "Unknown", "Youtube", "Unknown", "Tiktok", "Facebook", "Google"])
  user_agent = generate_user_agent()
  ip_address = generate_ip_address()
  event_timestamp = datetime.now()
  
  click_event = {
    'click_id': click_id,
    'user_id': user_id,
    'source': source,
    'user_agent': user_agent,
    'ip_address': ip_address,
    'click_timestamp': event_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
  }
  
  return click_event


# Generate checkout events with the current event_timestamp
def generate_checkout_event(user_id: int, product_id: int) -> dict:
  checkout_id = str(uuid4())
  quantity = random.randint(1, 5)
  shipping_cost = round(random.uniform(1.0, 10.0), 2) # Random value between [1.00, 10.00] USD
  discount = round(random.uniform(0.05, 0.5), 2) # Random value between [5, 50] percentage
  payment_method = random.choice(["Visa", "MasterCard", "Stripe", "Payment on Delivery", 
                                "Paypal", "Alipay", "Skrill"])
  # 20% of the time payment is failed
  if random.randint(1, 100) >= 80:
    payment_status = "Failed"
  else:
    payment_status = "Success"
  payment_description = random.choice(["Insufficient Fund", "Invalid Payment Details", "Network Connectivity Issues",
                                "Payment Gateway Issues", "Incorrect Billing Address", "Card Expired"]) if payment_status == "Failed" else "None"
  shipping_address = fake.address()
  event_timestamp = datetime.now()
  
  checkout_event = {
    'checkout_id': checkout_id,
    'user_id': user_id,
    'product_id': product_id,
    'quantity': quantity,
    'shipping_cost': shipping_cost,
    'discount': discount,
    'payment_method': payment_method,
    'payment_status': payment_status,
    'payment_description': payment_description,
    'shipping_address': shipping_address,
    'checkout_timestamp': event_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
  }
  
  return checkout_event
  
  
# Generate click datastream
def generate_click_datastream() -> None:
  click_event = generate_click_event(None)
  push_to_kafka(click_event, 'clicks')
  
  # 50% of the time is checkouts
  while random.randint(1, 100) <= 50:
    checkout_event = generate_checkout_event(click_event['user_id'], get_random_product_id())
    push_to_kafka(checkout_event, 'checkouts')


if __name__ == '__main__':
  n = 10000
  while n > 0:
    n -= 1
    generate_click_datastream()
    time.sleep(1)
    print(f'Generated {n} events')
    if n == 0:
      time.sleep(10)  # Sleep for 10 seconds before generating more data
      n = 10000
      