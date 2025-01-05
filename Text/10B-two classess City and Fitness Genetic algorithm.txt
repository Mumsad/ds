import numpy as np
import matplotlib.pyplot as plt
import copy

# Cost function (Sphere function)
def sphere(x):
    return sum(x**2)

# Roulette Wheel Selection
def roulette_wheel_selection(p):
    c = np.cumsum(p)
    r = sum(p) * np.random.rand()
    ind = np.argwhere(r <= c)
    return ind[0][0]

# Crossover function (Uniform crossover)
def crossover(p1, p2):
    c1 = copy.deepcopy(p1)
    c2 = copy.deepcopy(p2)
    alpha = np.random.uniform(0, 1, *(c1['position'].shape))
    c1['position'] = alpha * p1['position'] + (1 - alpha) * p2['position']
    c2['position'] = alpha * p2['position'] + (1 - alpha) * p1['position']
    return c1, c2

# Mutation function (Gaussian mutation)
def mutate(c, mu, sigma):
    y = copy.deepcopy(c)
    flag = np.random.rand(*(c['position'].shape)) <= mu  # array of True and False, indicating where mutation occurs
    ind = np.argwhere(flag)
    y['position'][ind] += sigma * np.random.randn(*ind.shape)
    return y

# Bound the values within the given range
def bounds(c, varmin, varmax):
    c['position'] = np.maximum(c['position'], varmin)
    c['position'] = np.minimum(c['position'], varmax)

# Sorting the population based on cost
def sort_population(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j]['cost'] > arr[j + 1]['cost']:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Genetic Algorithm Main Function
def ga(costfunc, num_var, varmin, varmax, maxit, npop, num_children, mu, sigma, beta):
    population = {}
    for i in range(npop):
        population[i] = {'position': None, 'cost': None}  # Initialize individuals with position and cost

    # Best solution found
    bestsol = copy.deepcopy(population)
    bestsol_cost = np.inf  # initial best cost is infinity

    # Initialize population - 1st Generation
    for i in range(npop):
        population[i]['position'] = np.random.uniform(varmin, varmax, num_var)
        population[i]['cost'] = costfunc(population[i]['position'])
        if population[i]['cost'] < bestsol_cost:
            bestsol = copy.deepcopy(population[i])
            bestsol_cost = population[i]['cost']

    bestcost = np.empty(maxit)

    # Main loop for the GA
    for it in range(maxit):
        # Calculate probability for roulette wheel selection
        costs = [population[i]['cost'] for i in range(len(population))]
        costs = np.array(costs)
        avg_cost = np.mean(costs)
        if avg_cost != 0:
            costs = costs / avg_cost
        probs = np.exp(-beta * costs)

        # Selection and reproduction
        for _ in range(num_children // 2):
            # Roulette wheel selection for parents
            p1 = population[roulette_wheel_selection(probs)]
            p2 = population[roulette_wheel_selection(probs)]
            
            # Crossover to produce children
            c1, c2 = crossover(p1, p2)
            
            # Mutation of children
            c1 = mutate(c1, mu, sigma)
            c2 = mutate(c2, mu, sigma)
            
            # Apply bounds to children
            bounds(c1, varmin, varmax)
            bounds(c2, varmin, varmax)

            # Evaluate cost of the children
            c1['cost'] = costfunc(c1['position'])
            if c1['cost'] < bestsol_cost:
                bestsol = copy.deepcopy(c1)
                bestsol_cost = c1['cost']
            
            c2['cost'] = costfunc(c2['position'])
            if c2['cost'] < bestsol_cost:
                bestsol = copy.deepcopy(c2)
                bestsol_cost = c2['cost']

            # Add the new children to the population
            population[len(population)] = c1
            population[len(population)] = c2

        # Sort the population based on the cost
        population = sort_population(population)

        # Store best cost of the current iteration
        bestcost[it] = bestsol_cost

        # Print the iteration results
        print(f'Iteration {it}: Best Cost = {bestcost[it]}')

    return population, bestsol, bestcost

# Problem definition
costfunc = sphere
num_var = 5  # Number of decision variables
varmin = -10  # Lower bound
varmax = 10  # Upper bound

# GA Parameters
maxit = 501
npop = 20  # Population size
beta = 1  # Beta value for cost scaling
prop_children = 1  # Proportion of children to population
num_children = int(np.round(prop_children * npop / 2) * 2)  # Ensure it's even
mu = 0.2  # Mutation rate
sigma = 0.1  # Mutation step size

# Run GA
out = ga(costfunc, num_var, varmin, varmax, maxit, npop, num_children, mu, sigma, beta)

# Plot results
plt.plot(out[2])
plt.xlim(0, maxit)
plt.xlabel('Generations')
plt.ylabel('Best Cost')
plt.title('Genetic Algorithm')
plt.grid(True)
plt.show()
