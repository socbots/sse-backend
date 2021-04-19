import sseclient

messages = sseclient.SSEClient('http://localhost:5000/stream')

for msg in messages:
    print(msg)
