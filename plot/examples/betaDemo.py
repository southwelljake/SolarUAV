import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

data = [0.2, 0.3, 0.5, 0.6, 0.9]
mean = np.mean(data)
var = np.var(data)

a = mean * (mean * (1 - mean) / var - 1)
b = (1 - mean) * (mean * (1 - var) / var - 1)

fig4, ax4 = plt.subplots()

ax4.plot(beta.pdf(np.linspace(0, 1, 100), a, b))
ax4.plot([100 * d for d in data], [0 for p in range(0, len(data))], 'xr')
ax4.set_xlabel('Cloud Cover (%)')
ax4.set_ylabel('PDF')

plt.show()