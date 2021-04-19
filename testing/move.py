import time
import requests

while True:
    input("POST a move... Press enter")
    res = requests.post('http://localhost:5000/move', json={"gesture":"wave"})
    if res.ok:
        print(res.json())