import time
import requests

while True:
    input("Send a ping... Press the any key")
    requests.get('https://alfsse.herokuapp.com/ping')
