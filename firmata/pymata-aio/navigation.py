#!/usr/bin/env python
# encoding: utf-8
"""
Control Navigation Features
"""

# from pixy import *

class Navigation():
  def __init__(self):
    # TODO
    return None

  def with_pixy(self, pixy_data):
    # TODO
    return None

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
