import time
import requests


print("\
1. Wave right hand\n\
2. Move head up distance 3")

while True:
    selection = str(input("POST a move... "))

    if selection == "q":
        break

    commands = {
        "1": {
            "gesture": "wave", 
            "bodyPart": "right_hand"
            },
        "2": {
            "direction": "up", 
            "bodyPart": "head",
            "distance": 3
            },
    }
    
    res = requests.post(
        "https://alfsse.herokuapp.com/move", json=commands[selection]
    )


    if res.ok:
        print(res.json())
