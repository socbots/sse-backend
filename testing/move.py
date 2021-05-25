import time
import requests



while True:
    input("POST a move... Press enter")
    
    res = requests.post(
        "http://alfsse.herokuapp.com/move", json={
            "gesture": "wave", 
            "bodyPart": "right_hand"
            }
    )


    if res.ok:
        print(res.json())

"""    res = requests.post(
        "http://alfsse.herokuapp.com/move", json={
            "direction": "up", 
            "bodyPart": "head",
            "distance": 3
            }
    )
"""