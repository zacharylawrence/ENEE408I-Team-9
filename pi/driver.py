#!/usr/bin/env python
# encoding: utf-8
"""
Drive the Robot
"""

import sched, time
import signal, sys
import time
from enum import Enum

import constants
from arduino import Arduino
from navigation import Navigation

class State(Enum):
  COLLECT_spin_and_search_cone = 1
  COLLECT_wander_and_search_cone = 2
  COLLECT_approach_cone = 3
  COLLECT_acquire_cone = 4
  COLLECT_open_claw = 5
  DELIVER_spin_and_search_target = 6
  DELIVER_wander_and_search_target = 7
  DELIVER_approach_target = 8
  DELIVER_verify_target = 9
  DELIVER_release_cone = 10

class Driver():
  # Wait .05 sec between loops
  # This waits after the loop is run. This will not subtract the time it took to run loop() from the total wait time.
  def __init__(self, webserver_queue=None, looprate=0.2):
    self.arduino = Arduino()
    self.navigation = Navigation(self.arduino)
    self.state = State.COLLECT_spin_and_search_cone
    # Define constants
    self.looprate = looprate
    # Variables updated from webserver
    self.webserver_queue = webserver_queue
    self.mode = "auto"
    self.manual_direction = "stop"
    # Variables used by states
    self.start_time = None

  def start(self):
    self.stop = False

    s = sched.scheduler(time.time, self.arduino.board.sleep)
    s.enter(0, 1, self.loop, (s,))
    s.run()

  def stop_on_next_loop(self):
    self.stop = True

  def loop(self, sc):
    # Read webserver queue for new messages
    while((self.webserver_queue != None) and (len(self.webserver_queue) > 0)):
      self.process_message(self.webserver_queue.popleft())

    # If stopped, just loop
    if (self.stop):
      sc.enter(self.looprate, 1, self.loop, (sc,))
      return

    if (self.mode == "auto"):

      # ---- Collect Spin and Search Cone ----

      if (self.state == State.COLLECT_spin_and_search_cone):
        if (self.start_time == None):
          self.start_time = time.time()

        if (time.time() - self.start_time >= constants.SPIN_TIME):
          self.start_time = None
          self.navigation.stop()
          self.change_state(State.COLLECT_wander_and_search_cone)
        # TODO: Use signatures with pixy
        else:
          status = self.navigation.spin_and_search_cone()
          if (status == "CONE_FOUND"):
            self.start_time = None
            self.change_state(State.COLLECT_approach_cone)

      # ---- Collect Wander and Search ----

      elif (self.state == State.COLLECT_wander_and_search_cone):
        if (self.start_time == None):
          self.start_time = time.time()

        if (time.time() - self.start_time >= constants.WANDER_TIME):
          self.start_time = None
          self.navigation.stop()
          self.change_state(State.COLLECT_spin_and_search_cone)
        # TODO: Use signatures with pixy
        else:
          status = self.navigation.wander_and_search_cone()
          if (status == "CONE_FOUND"):
            self.start_time = None
            self.change_state(State.COLLECT_approach_cone)

      # ---- Collect Approach Cone ----

      elif (self.state == State.COLLECT_approach_cone):
        status = self.navigation.approach_cone()
        if (status == "LOST_CONE"):
          self.change_state(State.COLLECT_wander_and_search_cone)
        elif (status == "CONE_IN_RANGE"):
          self.change_state(State.COLLECT_acquire_cone)

      # ---- Collect Acquire Cone ----

      elif (self.state == State.COLLECT_acquire_cone):
        self.arduino.close_claw()

        ping = self.arduino.get_ping()
        if (ping <= constants.PING_CONE_THRESHOLD and ping != 0):
          self.change_state(State.DELIVER_spin_and_search_target)
        else:
          self.change_state(State.COLLECT_open_claw)

      # ---- Collect Open Claw ----

      elif (self.state == State.COLLECT_open_claw):
        self.arduino.open_claw()
        self.change_state(State.COLLECT_approach_cone)

      # ---- Deliver Spin and Search Target ----

      elif (self.state == State.DELIVER_spin_and_search_target):
        if (self.start_time == None):
          self.start_time = time.time()

        if (time.time() - self.start_time >= constants.SPIN_TIME):
          self.start_time = None
          self.navigation.stop()
          self.change_state(State.DELIVER_wander_and_search_target)
        # TODO: Use signatures with pixy
        else:
          status = self.navigation.spin_and_search_target()
          if (status == "TARGET_FOUND"):
            self.start_time = None
            self.change_state(State.DELIVER_approach_target)

      # ---- Deliver Wander and Search Target ----

      elif (self.state == State.DELIVER_wander_and_search_target):
        if (self.start_time == None):
          self.start_time = time.time()

        if (time.time() - self.start_time >= constants.WANDER_TIME):
          self.start_time = None
          self.navigation.stop()
          self.change_state(State.DELIVER_spin_and_search_target)
        # TODO: Use signatures with pixy
        else:
          status = self.navigation.wander_and_search_target()
          if (status == "TARGET_FOUND"):
            self.start_time = None
            self.change_state(State.DELIVER_approach_target)

      # ---- Deliver Approach Target ----

      elif (self.state == State.DELIVER_approach_target):
        status = self.navigation.approach_target()
        if (status == "LOST_TARGET"):
          self.change_state(State.DELIVER_wander_and_search_target)
        elif (status == "TARGET_IN_RANGE"):
          self.change_state(State.DELIVER_verify_target)

      # ---- Deliver Verify Target ----

      elif (self.state == State.DELIVER_verify_target):
        self.change_state(State.DELIVER_release_cone)

      # ---- Deliver Release Cone ----

      elif (self.state == State.DELIVER_release_cone):
        self.arduino.open_claw()
        self.arduino.board.sleep(1)

        self.navigation.reverse()
        self.arduino.board.sleep(5)

        self.navigation.spin_clockwise()
        self.arduino.board.sleep(3)

        print("Starting over...")
        self.change_state(State.COLLECT_spin_and_search_cone)

    elif (self.mode == "manual"):
      # print("In manual mode")
      if (self.manual_direction == "stop"):
        (left_motor, right_motor) = (0.0, 0.0)
      elif (self.manual_direction == "forward"):
        (left_motor, right_motor) = (0.2, 0.2)
      elif (self.manual_direction == "backward"):
        (left_motor, right_motor) = (-0.2, -0.2)
      elif (self.manual_direction == "right"):
        (left_motor, right_motor) = (0.2, 0.0)
      elif (self.manual_direction == "left"):
        (left_motor, right_motor) = (0.0, 0.2)

      print("L: " + str(left_motor) + " R: " + str(right_motor))
      self.arduino.set_motors(left_motor, right_motor)

    elif (self.mode == "kill"):
      self.shutdown()
      sys.exit(0)

    # Loop again after delay
    sc.enter(self.looprate, 1, self.loop, (sc,))

  def change_state(self, new_state):
    print("[State Change] " + str(self.state) + " -> " + str(new_state))
    self.state = new_state

  def process_message(self, message):
    if (message == "stop"):
      self.stop_on_next_loop()
    elif (message == "start"):
      self.start()
    elif (message == "print"):
      print("Print!")

    # Modes
    elif (message == "auto"):
      self.mode = "auto"
    elif (message == "manual"):
      self.mode = "manual"
    elif (message == "kill"):
      self.mode = "kill"

    # Manual Directions
    elif (message == "manual_forward"):
      self.manual_direction = "forward"
    elif (message == "manual_backward"):
      self.manual_direction = "backward"
    elif (message == "manual_right"):
      self.manual_direction = "right"
    elif (message == "manual_left"):
      self.manual_direction = "left"
    elif (message == "manual_stop"):
      self.manual_direction = "stop"

  def shutdown(self, signal=None, frame=None):
    self.arduino.shutdown()


if __name__ == '__main__':
  driver = Driver()

  # Graceful shutdown on ctrl-c
  signal.signal(signal.SIGINT, driver.shutdown)

  driver.start()
