#!/usr/bin/env python
# encoding: utf-8
"""
Start the Robot and Webserver
"""

from threading import Thread
from collections import deque
from flask import Flask
import signal, sys
import asyncio

from driver import Driver

app = Flask(__name__)
q = deque()

def robot_thread(event_kill):
  asyncio.set_event_loop(asyncio.new_event_loop())

  driver = Driver(webserver_queue=q)
  driver.start()

@app.route("/")
def hello():
  q.append("print")
  return "Hello World!"

@app.route("/stop")
def stop():
  q.append("stop")

@app.route("/start")
def start():
  q.append("start")

# Modes
@app.route("/mode/auto")
def auto():
  q.append("auto")

@app.route("/mode/manual")
def manual():
  q.append("manual")

# Manual Directions
@app.route("/manual/forward")
def manual_forward():
  q.append("manual_forward")

@app.route("/manual/backward")
def manual_backward():
  q.append("manual_backward")

@app.route("/manual/right")
def manual_right():
  q.append("manual_right")

@app.route("/manual/left")
def manual_left():
  q.append("manual_left")

@app.route("/manual/stop")
def manual_stop():
  q.append("manual_stop")

# @app.route("/manual/servo")
# def manual_servo():
#   val = requests.args.get(val)
#   q.append("manual")

def shutdown(signal=None, frame=None):
  q.append("stop")
  sys.exit(0)

if __name__ == "__main__":
  thread = Thread(target = robot_thread, args = (10, ))
  thread.start()

  signal.signal(signal.SIGINT, shutdown)

  app.run(host='0.0.0.0')
