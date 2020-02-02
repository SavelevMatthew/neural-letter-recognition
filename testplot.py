import matplotlib.pyplot as plt
import numpy as np
import os
a = np.zeros([3, 2])
a[0,0] = 1
a[1,1] = 3
print(a)
l = a.tolist()
print(l)
b = np.asfarray(l)
print(b)
#plt.imshow(a, interpolation='nearest')

with open(os.path.join('mnist_dataset', 'mnist_train_100.csv'), 'r') as f:
    data = f.readlines()
v = data[0].split(',')
img = np.asfarray(v[1:],).reshape((28, 28))
plt.imshow(img, cmap='Greys')
plt.show()
