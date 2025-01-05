import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the Seaborn color palette
sns.set_palette('Set2')

# Parameters
N = 400  # Number of neurons
P = 100  # Number of patterns
NO_OF_ITERATIONS = 40  # Number of iterations for testing
NO_OF_BITS_TO_CHANGE = 200  # Number of bits to change in the test pattern

# Generate random patterns
epsilon = np.asarray([np.random.choice([1, -1], size=N)])
for _ in range(P - 1):
    epsilon = np.append(epsilon, [np.random.choice([1, -1], size=N)], axis=0)

print(f"Epsilon shape: {epsilon.shape}")

# Select a random pattern for testing
random_pattern = np.random.randint(P)
test_array = epsilon[random_pattern].copy()

# Modify the first NO_OF_BITS_TO_CHANGE bits
random_pattern_test = np.random.choice([1, -1], size=NO_OF_BITS_TO_CHANGE)
test_array[:NO_OF_BITS_TO_CHANGE] = random_pattern_test

print(f"Random pattern index: {random_pattern}")

# Compute the weight matrix
w = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        for p in range(P):
            w[i, j] += epsilon[p, i] * epsilon[p, j]
        if i == j:
            w[i, j] = 0
w /= N

# Hamming distance calculation
hamming_distance = np.zeros((NO_OF_ITERATIONS, P))
h = np.zeros(N)

for iteration in range(NO_OF_ITERATIONS):
    for _ in range(N):
        i = np.random.randint(N)
        h[i] = 0
        for j in range(N):
            h[i] += w[i, j] * test_array[j]
        test_array[i] = -1 if h[i] < 0 else 1

    # Calculate the Hamming distance
    for i in range(P):
        hamming_distance[iteration, i] = ((epsilon[i] - test_array) != 0).sum()

# Plot Hamming Distance
fig = plt.figure(figsize=(8, 8))
for i in range(P):
    plt.plot(hamming_distance[:, i], label=f'Pattern {i + 1}')
plt.xlabel('Number of Iterations')
plt.ylabel('Hamming Distance')
plt.ylim([0, N])
plt.title('Hamming Distance over Iterations')
plt.legend(loc='upper right', fontsize='small', ncol=2)
plt.show()
