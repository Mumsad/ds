import numpy as np
import matplotlib.pyplot as plt

class SimpleSOM:
    def __init__(self, grid_size=(10, 10), input_dim=2, learning_rate=0.1, radius=1.0, iterations=100):
        self.grid_size = grid_size  # Size of the grid (rows x columns)
        self.input_dim = input_dim  # Number of features in the input data (2 for 2D data)
        self.learning_rate = learning_rate  # Learning rate for updating weights
        self.radius = radius  # Radius of neighborhood for weight updates
        self.iterations = iterations  # Number of iterations for training
        
        # Initialize the SOM grid with random weights
        self.weights = np.random.random((grid_size[0], grid_size[1], input_dim))
    
    def _find_bmu(self, data_point):
        """
        Find the Best Matching Unit (BMU) for the given data point.
        """
        # Calculate the Euclidean distance between data_point and all the neurons in the grid
        distances = np.linalg.norm(self.weights - data_point, axis=2)
        bmu_idx = np.unravel_index(np.argmin(distances), distances.shape)
        return bmu_idx
    
    def _update_weights(self, data_point, bmu_idx, iteration):
        """
        Update the weights of the SOM grid based on the BMU and its neighbors.
        """
        # Calculate the learning rate and radius for this iteration
        learning_rate = self.learning_rate * (1 - iteration / self.iterations)
        radius = self.radius * (1 - iteration / self.iterations)
        
        # Loop over all neurons in the grid
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                # Calculate the distance from the current neuron to the BMU
                dist = np.linalg.norm(np.array([i, j]) - np.array(bmu_idx))
                
                # Update the weights if within the neighborhood radius
                if dist <= radius:
                    influence = np.exp(-dist**2 / (2 * (radius**2)))
                    self.weights[i, j] += influence * learning_rate * (data_point - self.weights[i, j])
    
    def train(self, data):
        """
        Train the SOM using the input data.
        """
        for iteration in range(self.iterations):
            # Shuffle the data to ensure diverse training
            np.random.shuffle(data)
            
            # Update weights for each data point
            for data_point in data:
                bmu_idx = self._find_bmu(data_point)
                self._update_weights(data_point, bmu_idx, iteration)
    
    def visualize(self):
        """
        Visualize the trained SOM grid.
        """
        plt.imshow(np.linalg.norm(self.weights, axis=2))  # Visualize the norm of the weights as a color map
        plt.title("Self-Organizing Map")
        plt.colorbar()
        plt.show()

# Example usage:
if __name__ == "__main__":
    # Generate random 2D data points
    data = np.random.rand(100, 2)  # 100 random points in 2D space

    # Create and train the SOM
    som = SimpleSOM(grid_size=(10, 10), input_dim=2, learning_rate=0.1, radius=1.0, iterations=100)
    som.train(data)

    # Visualize the trained SOM
    som.visualize()
