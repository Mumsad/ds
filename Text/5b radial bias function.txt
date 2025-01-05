from scipy.linalg import norm, pinv
from matplotlib import pyplot as plt
import numpy as np
from numpy import random


class RBF:
    def __init__(self, indim, numCenters, outdim):
        self.indim = indim
        self.outdim = outdim
        self.numCenters = numCenters
        self.centers = [random.uniform(-1, 1, indim) for _ in range(numCenters)]
        self.beta = 8
        self.W = random.random((self.numCenters, self.outdim))

    def _basisfunc(self, c, d):
        assert len(d) == self.indim
        return np.exp(-self.beta * norm(c - d) ** 2)

    def _calcAct(self, X):
        # Calculate activations of RBFs
        G = np.zeros((X.shape[0], self.numCenters), float)
        for ci, c in enumerate(self.centers):
            for xi, x in enumerate(X):
                G[xi, ci] = self._basisfunc(c, x)
        return G

    def train(self, X, Y):
        """Train the RBF model.
        X: matrix of dimensions n x indim
        Y: column vector of dimension n x 1
        """
        # Choose random center vectors from training set
        rnd_idx = random.permutation(X.shape[0])[:self.numCenters]
        self.centers = [X[i, :] for i in rnd_idx]
        print("Centers:", self.centers)
        # Calculate activations of RBFs
        G = self._calcAct(X)
        print("Activations (G):", G)
        # Calculate output weights (pseudo-inverse)
        self.W = np.dot(pinv(G), Y)

    def test(self, X):
        """Test the RBF model.
        X: matrix of dimensions n x indim
        """
        G = self._calcAct(X)
        Y = np.dot(G, self.W)
        return Y


if __name__ == "__main__":
    # 1D Example
    n = 100
    x = np.mgrid[-1:1:complex(0, n)].reshape(n, 1)
    # Set y and add random noise
    y = np.sin(3 * (x + 0.5) ** 3 - 1)
    y += random.normal(0, 0.1, y.shape)

    # RBF Regression
    rbf = RBF(1, 10, 1)
    rbf.train(x, y)
    z = rbf.test(x)

    # Plot original data
    plt.figure(figsize=(12, 8))
    plt.plot(x, y, 'k-', label="Original Data")
    # Plot learned model
    plt.plot(x, z, 'r-', linewidth=2, label="Learned Model")
    # Plot RBF centers
    plt.plot([c[0] for c in rbf.centers], np.zeros(rbf.numCenters), 'gs', label="RBF Centers")
    for c in rbf.centers:
        c_scalar = c[0]  # Extract scalar value from center
        ix = np.arange(c_scalar - 0.7, c_scalar + 0.7, 0.01)
        iy = [rbf._basisfunc(np.array([ix_]), np.array([c_scalar])) for ix_ in ix]
        plt.plot(ix, iy, '-', color='gray', linewidth=0.2)

    plt.xlim(-1.2, 1.2)
    plt.legend()
    plt.show()
