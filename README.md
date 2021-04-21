# API for making Sanbot move
*Make Alf do your biddings without touching Java code.*

### How dis work?

**sse_backend** is a Flask app that serves an [SSE](https://en.wikipedia.org/wiki/Server-sent_events) stream on the endpoint **/stream**.
It listens for a POST request to **/move**, which then sends off the JSON data to be emitted at /stream => **MobileSDK** is connected and listens for changes at /stream
=> this event gets parsed and sends move commands to **Sanbot**.

## Usage
POST to /move accepts the following JSON properties:

```
{
  bodyPart: String
  gesture: String
  direction: String
  distance: int
}
```
bodyPart is:
- head
- left_hand
- right_hand
- feet

direction is:
- left
- right
- up
- down
- stop

gesture accepts currently:
- wave

All properties aren't needed, it depends what you want the robot to do

### Make Alf wave
```
POST http://<sse_backend_url>/move HTTP/1.1
content-type: application/json


{
  "gesture": "wave",
  "bodyPart": "left_hand"
}
```
Waving requires just the gesture and which bodypart.
Alf can wave any part of his body! Even the feet! Try it out :)


### Can't be bothered with postman?
For quick testing, slam this into chromes console:
```
fetch('http://<sse_backend_url:5000/move', {
  method: 'POST',
  body: JSON.stringify({
    gesture: 'wave',
    bodyPart: 'left_hand'
  }),
  headers: {
    'Content-type': 'application/json; charset=UTF-8'
  }
})
.then(res => res.json())
.then(console.log)
```
Remember you need to have the MobileSDK running to see the results, but this will get you a json response if your sse_server is working.

- - -

Other emotes should be easy to implement now that we have the framework on MobileSDK setup.
Moving bodyparts a specific direction and distance aren't supported yet!
