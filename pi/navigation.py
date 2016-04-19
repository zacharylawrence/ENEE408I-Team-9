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
    self.arduino.set_motors(constants.FORWARD_SPEED_LEFT, constants.FORWARD_SPEED_RIGHT)

  def spin_clockwise(self):
    self.arduino.set_motors(constants.SPIN_SPEED_LEFT, -1 * constants.SPIN_SPEED_RIGHT)

  def spin_counterclockwise(self):
    self.arduino.set_motors(-1 * constants.SPIN_SPEED_LEFT, constants.SPIN_SPEED_RIGHT)

  def spin_clockwise_fast(self):
    self.arduino.set_motors(constants.SPIN_SPEED_LEFT_FAST, -1 * constants.SPIN_SPEED_RIGHT_FAST)

  def spin_counterclockwise_fast(self):
    self.arduino.set_motors(-1 * constants.SPIN_SPEED_LEFT_FAST, constants.SPIN_SPEED_RIGHT_FAST)

  def spin_and_search_cone(self):
    if (self.pixy.signature_name != "cone"):
      self.pixy.set_signature_cone()

    block_x = self.pixy.get_pixy_block_x_average(self.arduino.get_pixy_blocks())

    if (block_x != None):
      print("Cone Found")
      self.stop()
      return "CONE_FOUND"
    else:
      self.spin_clockwise_fast()
      return None

  # def wander_and_search_cone(self):
  #   if (self.pixy.signature_name != "cone"):
  #     self.pixy.set_signature_cone()

  #   block_x = self.pixy.get_pixy_block_x_average(self.arduino.get_pixy_blocks())

  #   if (block_x != None):
  #     print("Cone Found")
  #     self.stop()
  #     return "CONE_FOUND"
  #   else:
  #     self.spin_counterclockwise()
  #     return None

  def wander_and_search_cone(self):
    if (self.pixy.signature_name != "cone"):
      self.pixy.set_signature_cone()

    block_x = self.pixy.get_pixy_block_x_average(self.arduino.get_pixy_blocks())
    self.arduino.print_ir()
    if (block_x != None):
      print("Cone Found")
      self.stop()
      return "CONE_FOUND"
    else:
      if (self.arduino.ir_wall()):
        print("Wandered into wall! Spinning...")
        self.spin_clockwise_fast()
      else:
        self.forward()
      return None

  # Returns "CONE_IN_RANGE" if cone in range, "LOST_CONE" if lose cone, otherwise None
  def approach_cone(self):
    if (self.pixy.signature_name != "cone"):
      self.pixy.set_signature_cone()

    block_x = self.pixy.get_pixy_block_x_average(self.arduino.get_pixy_blocks())
    ping = self.arduino.get_ping()

    if (block_x == None):
      print("Lost Cone")
      self.stop()
      return "LOST_CONE"

    if (ping <= constants.PING_CONE_THRESHOLD and ping != 0):
      print("Cone in Range")
      self.stop()
      return "CONE_IN_RANGE"

    print("x:" + str(block_x))
    if (block_x < constants.PIXY_BOUNDARY_LEFT):
      print("Go left")
      self.spin_counterclockwise()
      return None
    elif(block_x > constants.PIXY_BOUNDARY_RIGHT):
      print("Go right")
      self.spin_clockwise()
      return None
    else:
      print("Go forward")
      self.forward()
      return None

  def spin_and_search_target(self):
    if (self.pixy.signature_name != "target"):
      self.pixy.set_signature_target()

    block_x = self.pixy.get_pixy_block_x_average(self.arduino.get_pixy_blocks())

    if (block_x != None):
      print("Target Found")
      self.stop()
      return "TARGET_FOUND"
    else:
      self.spin_clockwise()
      return None

  def wander_and_search_target(self):
    if (self.pixy.signature_name != "target"):
      self.pixy.set_signature_target()

    block_x = self.pixy.get_pixy_block_x_average(self.arduino.get_pixy_blocks())

    if (block_x != None):
      print("Target Found")
      self.stop()
      return "TARGET_FOUND"
    else:
      self.spin_counterclockwise()
      return None

  # Returns "TARGET_IN_RANGE" if target in range, "LOST_TARGET" if lose target, otherwise None
  def approach_target(self):
    if (self.pixy.signature_name != "target"):
      self.pixy.set_signature_target()

    block_x = self.pixy.get_pixy_block_x_average(self.arduino.get_pixy_blocks())
    ping = self.arduino.get_ping()

    if (block_x == None):
      print("Lost Target")
      self.stop()
      return "LOST_TARGET"

    if (ping <= constants.PING_CONE_THRESHOLD and ping != 0):
      print("Target in Range")
      self.stop()
      return "TARGET_IN_RANGE"

    print("x:" + str(block_x))
    if (block_x < constants.PIXY_BOUNDARY_LEFT):
      print("Go left")
      self.spin_counterclockwise()
      return None
    elif(block_x > constants.PIXY_BOUNDARY_RIGHT):
      print("Go right")
      self.spin_clockwise()
      return None
    else:
      print("Go forward")
      self.forward()
      return None
