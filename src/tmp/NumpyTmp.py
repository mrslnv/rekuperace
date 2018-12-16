import numpy as np

a = np.arange(24)

a = a.reshape((4,6))

print(a)

a[0,2:] = a[0,1:-1]

print(a)

print(np.sum(a[0,1:5]))