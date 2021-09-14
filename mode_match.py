import matplotlib.pyplot as plt
plt.ion()
import numpy as np
import math

def get_length(p1, p2):
    x, y = abs(p1[0] - p2[0]), abs(p1[1] - p2[1])
    return (x*x + y*y)**0.5

def get_slope(p1, p2):
    return (p2[1] - p1[1]) / (p2[0] - p1[0])

class ModeMatch:
   W = []
   M = []
   lengths = []
   slopes = []
   cate_con = []

   def __init__(self, extreme):
       n = len(extreme)
       for i in range(0, n - 1):
           self.lengths.append(get_length(extreme[i], extreme[i+1]))
           self.slopes.append(get_slope(extreme[i], extreme[i+1]))
       return

   def fit(self):

       return

   def predict(self):
       return