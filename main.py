from client import *
prices = {}
alerts = []


client = websocket_client('ws://localhost:5000', prices, alerts)
client.start()








