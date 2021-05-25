import time
import requests



while True:
    input("POST a move... Press enter")
    
    """ res = requests.post(
        "http://localhost:5000/move", json={
            "gesture": "wave", 
            "bodyPart": "right_hand"
            }
    )
     """

    res = requests.post(
        "http://localhost:5000/move", json={
            "direction": "up", 
            "bodyPart": "head",
            "distance": 3
            }
    )
    if res.ok:
        print(res.json())
