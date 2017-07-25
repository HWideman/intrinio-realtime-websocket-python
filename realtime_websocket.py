# basis: - https://github.com/jorymorrison/real-time-intrinio-python/blob/master/realtime.py
from requests.auth import HTTPBasicAuth
import websocket
import threading
import requests
import base64
import json
import sys
import os

os.environ['INTRINIO_USER'] = ''
os.environ['INTRINIO_PASSWORD'] = ''

SECURITIES_ = sys.argv[1:len(sys.argv)]

try:
    print "Using Tickers: " + str(SECURITIES_)
except:
    print "Please include at least one ticker as argument"
    sys.exit()

auth_url = "https://realtime.intrinio.com/auth"
r = requests.get(auth_url, headers={"Authorization": "Basic %s" % base64.b64encode(os.environ['INTRINIO_USER'] + ":" + os.environ['INTRINIO_PASSWORD'])})
socket_target = "wss://realtime.intrinio.com/socket/websocket?token=%s" % (r.text)

def on_message(ws, message):
  try:
    result = json.loads(message)
    print result["payload"]
  except:
    print "##EXCEPTION IN MESSAGE JSON DECODE##"
    print message

def on_error(ws, error):
  print "##ERROR## " + error

def on_close(ws):
  print "##CONNECTION CLOSED##"

def on_open(ws):
  def run():
    for security in SECURITIES_:
      topic = "iex:securities:" + str(security).upper()
      message = json.dumps({"topic": topic,"event": "phx_join","payload": {},"ref": "1"})
      ws.send(message)
  threading.Thread(target=run).start()
  def heartbeat(init=False):
    t = threading.Timer(20.0, heartbeat); t.setDaemon(True); t.start()
    if init:
      return
    message = json.dumps({"topic": "phoenix","event": "heartbeat","payload": {},"ref": None})
    ws.send(message)
  heartbeat(init=True)

websocket.enableTrace(True)
ws = websocket.WebSocketApp(socket_target, on_message = on_message, on_error = on_error, on_close = on_close)
ws.on_open = on_open
ws.run_forever()
