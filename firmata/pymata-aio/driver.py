#!/usr/bin/env python
# encoding: utf-8
"""
Drive the Robot
"""

import sched, time
import signal, sys
from arduino import Arduino
from navigation import Navigation


class Driver():
  # Wait .05 sec between loops
  # This waits after the loop is run. This will not subtract the time it took to run loop() from the total wait time.
  def __init__(self, looprate=0.05):
    self.arduino = Arduino()
    self.navigation = Navigation()
    # Define constants
    self.looprate = looprate
    # Variables updated from webserver:
    self.stop = False

  def start(self):
    self.stop = False

    s = sched.scheduler(time.time, self.arduino.board.sleep)
    s.enter(0, 1, self.loop, (s,))
    s.run()

  def stop(self):
    self.stop = True

  def loop(self, sc):
    # print("New Loop")

    # Ping:
    # (left_motor, right_motor) = self.navigation.hold_ping(self.arduino.get_ping())

    # Pixy:
    (left_motor, right_motor) = self.navigation.with_pixy(self.arduino.get_pixy_blocks())

    # print("L: " + str(left_motor) + " R: " + str(right_motor))
    self.arduino.set_motors(left_motor, right_motor)


    # Loop again after delay
    if (self.stop):
      self.shutdown()
    else:
      sc.enter(self.looprate, 1, self.loop, (sc,))

  def shutdown(self, signal, frame):
    self.arduino.shutdown()
    sys.exit(0)


if __name__ == '__main__':
  driver = Driver()

  # Graceful shutdown on ctrl-c
  signal.signal(signal.SIGINT, driver.shutdown)

  driver.start()
