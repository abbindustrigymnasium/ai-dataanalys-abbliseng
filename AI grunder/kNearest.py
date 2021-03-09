import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib import style
import warnings
from collections import Counter

style.use("fivethirtyeight")

def eucdist(target, plot):
    euc = sqrt((plot[0]-target[0])**2 + (plot[1]-target[1])**2)
    print(euc)
    plt.scatter(plot[0],plot[1], s=150)

plot = [1,3]
target = [2,5]


plt.scatter(target[0],target[1], s=150)