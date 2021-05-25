import time
import requests

while True:
    input("Send a ping... Press the any key")
    requests.get('http://alfsse.herokuapp.com/ping')
