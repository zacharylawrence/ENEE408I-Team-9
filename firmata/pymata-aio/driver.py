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
  def __init__(self, looprate):
    self.arduino = Arduino()
    self.navigation = Navigation()
    self.looprate = looprate

  def loop(self, sc):
    print("New Loop")

    # self.arduino.blink_led()
    # self.arduino.set_motors(0.25, 0.25)
    print("Ping: " + str(self.arduino.get_ping()))
    # self.arduino.get_ping()

    (left_motor, right_motor) = self.navigation.hold_ping(self.arduino.get_ping())

    print("L: " + str(left_motor) + " R: " + str(right_motor))

    # Loop again after delay
    sc.enter(self.looprate, 1, self.loop, (sc,))

  def shutdown(self, signal, frame):
    self.arduino.shutdown()
    sys.exit(0)


if __name__ == '__main__':
  # Wait .05 sec between loops
  # This waits after the loop is run. This will not subtract the time it took to run loop() from the total wait time.
  driver = Driver(.05)

  # Graceful shutdown on ctrl-c
  signal.signal(signal.SIGINT, driver.shutdown)

  s = sched.scheduler(time.time, driver.arduino.board.sleep)
  s.enter(0, 1, driver.loop, (s,))
  s.run()
