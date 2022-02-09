#%%

import flask
from flask import request, jsonify
from flask_cors import CORS
import time
import json
import queue
import os


# https://maxhalford.github.io/blog/flask-sse-no-deps/
class MessageAnnouncer:
    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
                print("Announced msg:", msg)
            except queue.Full:
                print("Queue full, deleting listener number", self.listeners[i])
                del self.listeners[i]
            except Exception as e:
                print("Encountered unknown exception:", e)


config = {"DEBUG": True}  # some Flask specific configs

app = flask.Flask(__name__)
CORS(app)
# Add conf file to app
# app.config.from_mapping(config)
announcer = MessageAnnouncer()


def format_sse(data, event=None):
    msg = f"data: {data}\n\n"
    if event is not None:
        msg = f"event: {event}\n{msg}"
    return msg


@app.route("/ping")
def ping():
    msg = format_sse(data="pong")
    announcer.announce(msg=msg)
    return "PONG", 200


# Listens to POSTs to /move and announces the json data
@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    msg = format_sse(data)
    announcer.announce(msg=msg)
    return jsonify(data), 200


@app.route("/")
def hello_there():
    return (
        "<html><body><html><body><marquee><h1>You are on the SocBots Flask backend</h1></marquee></body></html></body></html>",
        200,
    )


@app.route("/stream")
def stream():
    def eventStream():
        messages = announcer.listen()
        while True:
            msg = messages.get()
            yield msg

    return app.response_class(eventStream(), mimetype="text/event-stream")


if __name__ == "__main__":
    pp = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=pp)
    print("Listening on port", pp)