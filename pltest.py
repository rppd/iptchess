#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 18:09:03 2020

@author: robin
"""

from matplotlib import pyplot as plt
from time import sleep

plt.axis([0,100,0,100])
img2 = plt.imread("sprites/sprite_02.png")
img3 = plt.imread("sprites/sprite_03.png")
cell = plt.imshow(img3, extent=[20,30,20,30])
plt.show()