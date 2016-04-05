#!/usr/bin/env python
# encoding: utf-8
"""
Control Navigation Features
"""

import constants
from pixy import Pixy

class Navigation():
  def __init__(self, arduino):
    self.pixy = Pixy()
    self.arduino = arduino

  def stop(self):
    self.arduino.set_motors(0, 0)

  def forward(self):
    self.arduino.set_motors(FORWARD_SPEED_LEFT, FORWARD_SPEED_RIGHT)

  def spin_clockwise(self):
    self.arduino.set_motors(SPIN_SPEED_LEFT, -1 * SPIN_SPEED_RIGHT)

  def spin_counterclockwise(self):
    self.arduino.set_motors(-1 * SPIN_SPEED_LEFT, SPIN_SPEED_RIGHT)

  def with_pixy(self, pixy_blocks):
    block = self.pixy.get_pixy_block(pixy_blocks)
    if (block == None):
      print("Could not get pixy data")
      return (0.0, 0.0)

    print("x:" + str(block["x"]))
    if (block["x"] < 100):
      print("Go left")
      return (-0.25, 0.25)
    elif(block["x"] > 200):
      print("Go right")
      return (0.25, -0.25)
    else:
      return (0.25, 0.25)

  def with_pixy_average(self, pixy_blocks):
    block_x = self.pixy.get_pixy_block_x_average(pixy_blocks)
    if (block_x == None):
      print("Could not get pixy data")
      return (0.0, 0.0)

    left_speed = 0.2
    right_speed = 0.2

    print("x:" + str(block_x))
    if (block_x < 100):
      print("Go left")
      return (-0.2, 0.2)
    elif(block_x > 200):
      print("Go right")
      return (0.2, -0.2)
    else:
      print("Go forward")
      return (0.2, 0.2)

  def with_pixy_average_and_ping(self, pixy_blocks, ping):
    block_x = self.pixy.get_pixy_block_x_average(pixy_blocks)
    if (block_x == None):
      print("Could not get pixy data")
      return (0.0, 0.0)

    print("x:" + str(block_x))
    if (block_x < 100):
      print("Go left")
      return (-0.2, 0.2)
    elif(block_x > 200):
      print("Go right")
      return (0.2, -0.2)
    else:
      if (ping >= 20 or ping == 0):
        print("Go forward")
        return (0.2, 0.2)
      else:
        print("Found cone")
        return (0.0, 0.0)

  # Return left/right motor speeds
  def hold_ping(self, distance):
    if (distance == None):
      return (0, 0)

    if (distance < 20):
      return (-0.1, -0.1)
    elif (distance > 20):
      return (0.1, 0.1)
    else:
      return (0, 0)
