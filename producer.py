import json
import time
import random
from datetime import datetime, timezone
from confluent_kafka import Producer

# Kafka Configuration
conf = {
    'bootstrap.servers': 'localhost:29092',
    'client.id': 'manning-market-producer'
}

producer = Producer(conf)
topic = 'market-prices'

# Sri Lankan Vegetables (Manning Market)
VEGETABLES = [
    {"name": "Carrot", "base_price": 180},
    {"name": "Leeks", "base_price": 150},
    {"name": "Cabbage", "base_price": 120},
    {"name": "Beans", "base_price": 250},
    {"name": "Tomato", "base_price": 300},
    {"name": "Brinjal", "base_price": 200},
    {"name": "Green Chilli", "base_price": 600},
    {"name": "Pumpkin", "base_price": 80},
]

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def generate_price_update():
    veg = random.choice(VEGETABLES)
    # Simulate price fluctuation (±10%)
    price_change = random.uniform(-0.1, 0.1)
    current_price = round(veg["base_price"] * (1 + price_change), 2)
    
    data = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "item_name": veg["name"],
        "unit": "1kg",
        "price": current_price,
        "market": "Manning Market, Colombo",
        "region": "Western Province"
    }
    return data

def main():
    print("Starting Sri Lankan Market Data Producer...")
    try:
        while True:
            data = generate_price_update()
            producer.produce(
                topic, 
                key=data["item_name"], 
                value=json.dumps(data).encode('utf-8'),
                callback=delivery_report
            )
            producer.flush()
            print(f"Sent: {data['item_name']} @ {data['price']} LKR")
            
            # Stream data every 1-3 seconds
            time.sleep(random.uniform(1, 3))
    except KeyboardInterrupt:
        print("Producer stopped.")

if __name__ == "__main__":
    main()
