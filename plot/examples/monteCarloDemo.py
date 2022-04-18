import matplotlib.pyplot as plt
import numpy as np

x_1 = []
y_1 = []

for x in range(0, 20):
    for y in range(0, 20):
        x_1.append(x)
        y_1.append(y)

x_2 = []
y_2 = []

for i in range(0, 200):
    x_2.append(np.random.uniform(0, 20))
    y_2.append(np.random.uniform(0, 20))

fig, ax = plt.subplots(ncols=2)

ax[0].plot(x_1, y_1, 'x')
ax[0].set_title('Intervals 400 Samples')
ax[1].set_title('Monte Carlo 200 Samples')
ax[1].plot(x_2, y_2, 'x')

plt.show()
