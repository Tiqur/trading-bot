import threading
from client import *
prices = {}
alerts = []

# Initialize client
thread = threading.Thread(target=websocket_client, args=('ws://localhost:5000', prices, alerts))
thread.start()

while True:
    print(prices)



