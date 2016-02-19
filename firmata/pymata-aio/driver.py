#!/usr/bin/env python
# encoding: utf-8
"""
Drive the Robot
"""

import sched, time
from arduino import Arduino


class Driver():
  def __init__(self, looprate):
    self.arduino = Arduino()
    self.looprate = looprate

  def loop(self, sc):
    print("New Loop")

    # self.arduino.blink_led()
    # self.arduino.set_motors(0.25, 0.25)
    print("Ping: " + str(self.arduino.get_ping()))
    # self.arduino.get_ping()

    # Loop again after delay
    sc.enter(self.looprate, 1, self.loop, (sc,))

  def shutdown(self):
    self.arduino.shutdown()


if __name__ == '__main__':
  # Wait .05 sec between loops
  # This waits after the loop is run. This will not subtract the time it took to run loop() from the total wait time.
  driver = Driver(.05)

  s = sched.scheduler(time.time, driver.arduino.board.sleep)
  s.enter(0, 1, driver.loop, (s,))
  s.run()
