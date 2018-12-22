import numpy as np
import math


##########################################

def arraySliceAndShift():
    a = np.arange(24)
    a = a.reshape((4, 6))
    print(a)
    a[0, 2:] = a[0, 1:-1]
    print(a)
    print(np.sum(a[0, 1:5]))


arraySliceAndShift()
##########################################

def updateWhere():
    a = np.arange(24)
    a.resize([6,4])
    a[np.mod(a,8) == 0] = 100
    print(a)

updateWhere()