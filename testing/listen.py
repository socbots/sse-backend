import sseclient

messages = sseclient.SSEClient('https://alfsse.herokuapp.com/stream')

for msg in messages:
    print(msg)
