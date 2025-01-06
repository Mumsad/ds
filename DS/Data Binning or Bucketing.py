import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
np.random.seed(0)
mu = 90 
sigma = 25 
x = mu + sigma * np.random.randn(5000)  # Generate 5000 data points from a normal distribution
num_bins = 25
fig, ax = plt.subplots()
n, bins, patches = ax.hist(x, num_bins, density=1)
y = stats.norm.pdf(bins, mu, sigma)
ax.plot(bins, y, '--')
ax.set_xlabel('Example Data')
ax.set_ylabel('Probability Density')
sTitle = (r'Histogram ' + str(len(x)) + ' entries into ' + str(num_bins) + ' Bins: '
          r'$\mu=' + str(mu) + '$, $\sigma=' + str(sigma) + '$')
ax.set_title(sTitle)
fig.tight_layout()
sPathFig = 'C:/VKHCG/05-DS/4000-UL/0200-DU/DU-Histogram.png'
os.makedirs(os.path.dirname(sPathFig), exist_ok=True)  # Create directory if it doesn't exist
fig.savefig(sPathFig)
plt.show()
