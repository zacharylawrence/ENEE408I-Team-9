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

  def with_pixy(self, pixy_blocks):
    if (len(pixy_blocks) >= 1):
      block = pixy_blocks[0]
      print("x:" + str(block["x"]))
      if (block["x"] < 100):
        print("Go left")
        return(-0.1, 0.1)
      elif(block["x"] > 200):
        print("Go right")
        return(0.1, -0.1)
      else:
        return(0.0, 0.0)
    return(0.0, 0.0)

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
