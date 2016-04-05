#!/usr/bin/env python
# encoding: utf-8
"""
Drive the Robot
"""

import sched, time
import signal, sys
from enum import Enum

from arduino import Arduino
from navigation import Navigation

#Mode = Enum('locate', 'orient', 'approach')

class Driver():
  # Wait .05 sec between loops
  # This waits after the loop is run. This will not subtract the time it took to run loop() from the total wait time.
  def __init__(self, webserver_queue=None, looprate=0.05):
    self.arduino = Arduino()
    self.navigation = Navigation()
    # Define constants
    self.looprate = looprate
    # Variables updated from webserver:
    self.webserver_queue = webserver_queue
    #self.mode = Mode.locate
    self.mode = "auto"
    self.manual_direction = "stop"

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
      # Ping:
      # (left_motor, right_motor) = self.navigation.hold_ping(self.arduino.get_ping())

      # Pixy:
      # (left_motor, right_motor) = self.navigation.with_pixy(self.arduino.get_pixy_blocks())

      # print("L: " + str(left_motor) + " R: " + str(right_motor))
      # self.arduino.set_motors(left_motor, right_motor)
      # print("\n")

      # Pixy + Ping:
      # print("ping: " + str(self.arduino.get_ping()))
      # (left_motor, right_motor) = self.navigation.with_pixy_average_and_ping(self.arduino.get_pixy_blocks(), self.arduino.get_ping())
      # print("L: " + str(left_motor) + " R: " + str(right_motor))
      # self.arduino.set_motors(left_motor, right_motor)
      # self.arduino.set_servo(servo)

      self.arduino.getA0()

    #   (left_motor, right_motor) = self.navigation.with_pixy_average(self.arduino.get_pixy_blocks())

    #   ping = self.arduino.get_ping()
    #   if (ping != None):
    #     if (ping != 0 and ping <= 5):
    #       self.arduino.close_claw()
    #       self.arduino.board.sleep(2)
    #       left_motor = -0.2
    #       right_motor = -0.2
    #     else:
    #       self.arduino.open_claw()
    #   # print(ping)

    #   print("L: " + str(left_motor) + " R: " + str(right_motor))
    #   self.arduino.set_motors(left_motor, right_motor)

    # elif (self.mode == "manual"):
    #   # print("In manual mode")
    #   if (self.manual_direction == "stop"):
    #     (left_motor, right_motor) = (0.0, 0.0)
    #   elif (self.manual_direction == "forward"):
    #     (left_motor, right_motor) = (0.2, 0.2)
    #   elif (self.manual_direction == "backward"):
    #     (left_motor, right_motor) = (-0.2, -0.2)
    #   elif (self.manual_direction == "right"):
    #     (left_motor, right_motor) = (0.2, 0.0)
    #   elif (self.manual_direction == "left"):
    #     (left_motor, right_motor) = (0.0, 0.2)

    #   print("L: " + str(left_motor) + " R: " + str(right_motor))
    #   self.arduino.set_motors(left_motor, right_motor)


    # # Loop again after delay
    if (self.stop):
      self.shutdown()
    else:
      sc.enter(self.looprate, 1, self.loop, (sc,))

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
