import random
import json
from datetime import datetime, timedelta
import time

# Stock symbols
STOCKS = ["AAPL", "GOOG", "TSLA", "AMZN", "MSFT"]

# Event types
EVENT_TYPES = ["price_update", "trade"]

# Market sentiment
SENTIMENTS = ["bullish", "bearish", "neutral"]

def generate_price(base_price):
    change = random.uniform(-2, 2)
    return round(base_price + change, 2)

def generate_event(symbol, base_price):
    event_type = random.choice(EVENT_TYPES)

    price = generate_price(base_price)
    volume = random.randint(100, 10000)

    event = {
        "symbol": symbol,
        "event_type": event_type,
        "price": price,
        "volume": volume,
        "market_sentiment": random.choice(SENTIMENTS),
        "timestamp": (datetime.now() - timedelta(seconds=random.randint(0, 3600)))
        .strftime("%Y-%m-%d %H:%M:%S")
    }

    return event, price


def generate_market_data(num_events=1000):
    data = []
    
    # Base prices for stocks
    base_prices = {
        "AAPL": 180,
        "GOOG": 2700,
        "TSLA": 250,
        "AMZN": 3300,
        "MSFT": 310
    }

    for _ in range(num_events):
        symbol = random.choice(STOCKS)
        event, new_price = generate_event(symbol, base_prices[symbol])
        
        # update base price (simulate market movement)
        base_prices[symbol] = new_price
        
        data.append(event)

    return data


if __name__ == "__main__":
    data = generate_market_data(2000)

    with open("data/raw/market_events.json", "w") as f:
        for record in data:
            f.write(json.dumps(record) + "\n")

    print("✅ Fresh clean data generated!")