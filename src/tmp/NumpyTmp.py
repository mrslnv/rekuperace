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


# arraySliceAndShift()
##########################################

def updateArray(what, deltaSinceLast, power):
    for a in range(what.shape[0]):
        updateRow(what[a], deltaSinceLast, power)


def updateRow(what, deltaSinceLast, power):
    period = what[0]
    lastPortion = what[1]
    newPortion = (lastPortion + deltaSinceLast) % period
    updates = math.floor((lastPortion + deltaSinceLast) / period) + 1
    updateCoefs = np.ones(min(updates, what.shape[0] - 2), what.dtype)
    if updates > 1:
        if updates > what.shape[0] - 2:
            what[2:] = 0
            updateCoefs[0] = newPortion / period
        else:
            what[updates + 1:] = what[2:-updates + 1]
            what[2:updates+1] = 0
            updateCoefs[-1] = (period - lastPortion) / period
            updateCoefs[0] = newPortion / period
    else:
        updateCoefs[0] = (newPortion - lastPortion) / period
    newUsage = updateCoefs * power
    what[2:2 + updates] += newUsage
    what[1] = newPortion


# sample = np.array([[60,0,0,20,20]],dtype=np.float64)
# print("0=",sample)
# # after 30s - 30
# updatePeriodPower(sample,30,30)
# print("computed=",sample)
# sample = np.array([[60, 30, 15, 20, 20]], dtype=np.float64)
# print("30s=", sample)
# # after 20s - 30
# # updates = [15]
# # updateCoefs = [2/6]
# # shift = 1
# updatePeriodPower(sample, 20, 30)
# print("computed=", sample)
# sample = np.array([[60, 50, 25, 20, 20]], dtype=np.float64)
# print("50s=", sample)
# # after 40s - 30
# updatePeriodPower(sample, 40, 30)
# print("computed=", sample)
# sample = np.array([60, 30, 15, 30, 20])
# print("50s=", sample)

# sample = np.array([[60, 0, 0, 25, 20]], dtype=np.float64)
# print("start=", sample)
# # after 60s - 30
# updateRow(sample, 60, 30)
# print("computed=", sample)
# sample = np.array([60, 0, 0, 30, 25])
# print("60s=", sample)

sample = np.array([[60, 0, 0, 0, 0, 0]], dtype=np.float64)
print("start=", sample)
updateArray(sample, 252, 40)
print("computed=", sample)
updateArray(sample, 48, 40)

sample = np.array([[60, 0, 0, 0, 0, 0],
                   [120, 0, 0, 0, 0, 0],
                   [180, 0, 0, 0, 0, 0],
                   [240, 0, 0, 0, 0, 0],
                   [600, 0, 0, 0, 0, 0]], dtype=np.float64)
print("start=", sample)
# after 60s - 30
updateArray(sample, 252, 40)
print("computed=", sample)
updateArray(sample, 48, 40)
print("computed=", sample)
updateArray(sample, 300, 40)
print("computed=", sample)

intervals = np.array([60, 120, 300, 600, 3600, 7200, 5 * 3600, 10 * 3600, 12 * 3600, 24 * 3600, 48 * 3600], np.float32)
# indexes = np.array([-1,0,0,2,3,4,4,6,5,8,9],np.int8)
# intervalRefs = np.concatenate([0],intervals[indexes[1:]])
# print("ir=",intervalRefs)

# lastPeriodPower = np.zeros([intervals.shape[0], 20], np.float32)
# lastPeriodPower[:, 0] = intervals
#
# updatePeriodPower(lastPeriodPower, 120, 20)
# print(lastPeriodPower)


##########################################
