#%%

import flask 
from flask_cors import CORS
import time
import json

app = flask.Flask(__name__)
CORS(app)

i = 0

def get_message():
  """
  global i
  time.sleep(2.0)
  if i % 2 == 0:
    s = {
      "time": 1800,
      "power": 8,
      "orientation": 1001
    }
  else:
    s = {
      "time": 600,
      "power": 3,
      "orientation": 1002
    }
  i += 1
  return s
  """

  foo_ = input("Type the body part to wave with(head, left_hand, right_hand)")
  wave = {
  "gesture": "wave",
  "body": foo_,
  "orientation": "up",
  }
  return wave




@app.route("/stream")
def stream():
  def eventStream():
        while True:
            # wait for source data to be available, then push it
            yield 'data: {}\n\n'.format(json.dumps(get_message()))

  return flask.Response(eventStream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(host="0.0.0.0") # 0.0.0.0 = listens on all addresses