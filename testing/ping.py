import time
import requests

while True:
    input("Send a ping... Press the any key")
    requests.get('http://localhost:5000/ping')
