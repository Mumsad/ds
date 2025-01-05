# In[1]:
# Get the number of elements
n = int(input("Enter number of elements: "))

# In[2]:
# Input values for 'inputs' list
print("Enter the inputs:")
inputs = [float(input(f"Input {i+1}: ")) for i in range(n)]

print("Inputs:", inputs)

# In[3]:
# Input values for 'weights' list
print("Enter the weights:")
weights = [float(input(f"Weight {i+1}: ")) for i in range(n)]

print("Weights:", weights)

# In[4]:
# Calculate and display the net input
print("The net input can be calculated as Yin = x1w1 + x2w2 + x3w3")

# In[5]:
# Calculate Yin
Yin = [inputs[i] * weights[i] for i in range(n)]
net_input = round(sum(Yin), 3)
print("Net input (Yin):", net_input)
