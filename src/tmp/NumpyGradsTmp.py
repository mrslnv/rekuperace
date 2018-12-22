import numpy as np
import math


##########################################


def updateWhere():
    a = np.arange(24)
    a.resize([6, 4])
    a[np.mod(a, 8) == 0] = 100
    print(a)


# updateWhere()


def roll():
    a = np.arange(24)
    a.resize([4, 6])
    print(a)
    # print(a[:,0])
    # print(np.mod(a[:,0], 4))
    # print(a[np.mod(a[:,0], 4) == 0,:])
    shiftedRowIndexes = np.mod(a[:, 0], 4) == 0
    a[shiftedRowIndexes, :] = np.roll(a[shiftedRowIndexes, :], 1, 1)
    print(a)


# print("roll")
# roll()

intervals = np.array([10, 20, 30, 60, 120])
grads = np.zeros((intervals.shape[0], 8))
grads[:, 0] = intervals


# int, temp, time, grad 1, grad 2, ...

def updateTemp(temp, tm):
    if grads[0, 2] == 0:
        grads[:, 2] = tm
        grads[:, 1] = temp
        return
    nextI = grads[:, 2] + grads[:, 0]
    shift = np.sign(tm - nextI)
    grads[shift >= 0, 3:] = np.roll(grads[shift >= 0, 3:], 1, 1)
    grads[shift >= 0, 3] = temp - grads[shift >= 0, 1]
    grads[shift >= 0, 1] = temp
    grads[shift >= 0, 2] = tm


updateTemp(2, 1)
print("2,1")
print(grads)
updateTemp(5, 11)
print("5,11")
print(grads)
updateTemp(7, 15)
print("7,15")
print(grads)
updateTemp(9, 22)
print("9,22")
print(grads)
updateTemp(12, 32)
print("12,32")
print(grads)
updateTemp(14, 42)
print("14,42")
print(grads)
updateTemp(15, 52)
print("15,52")
print(grads)
updateTemp(15.5, 62)
print("15.5,62")
print(grads)
