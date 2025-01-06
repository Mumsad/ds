import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Set the base directory for file paths
Base = r'C:\Users\kazis\Desktop\NOTES MSC P1\Prac\DS\VKHCG'

# Input and Output file paths
input_file = '02-Assess/01-EDS/02-Python/Assess-Network-Routing-Customer.csv'
output_file_gml = '06-Report/01-EDS/02-Python/Report-Network-Routing-Customer.gml'
output_file_png = '06-Report/01-EDS/02-Python/Report-Network-Routing-Customer.png'

# Load the customer data
customer_data = pd.read_csv(f"{Base}/{input_file}", encoding="latin-1")

# Display basic information about the data
print("First 5 rows of customer data:")
print(customer_data.head())

# Create a NetworkX graph
G = nx.Graph()

# Add edges between different customer countries
for i in range(customer_data.shape[0]):
    for j in range(customer_data.shape[0]):
        node_0 = customer_data['Customer_Country_Name'][i]
        node_1 = customer_data['Customer_Country_Name'][j]
        if node_0 != node_1:
            G.add_edge(node_0, node_1)

# Add additional edges: Country -> Place -> Coordinates
for i in range(customer_data.shape[0]):
    node_0 = customer_data['Customer_Country_Name'][i]
    node_1 = f"{customer_data['Customer_Place_Name'][i]}({customer_data['Customer_Country_Name'][i]})"
    node_2 = f"({customer_data['Customer_Latitude'][i]:.9f})({customer_data['Customer_Longitude'][i]:.9f})"
    if node_0 != node_1:
        G.add_edge(node_0, node_1)
    if node_1 != node_2:
        G.add_edge(node_1, node_2)

# Print the number of nodes and edges
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

# Save the graph to a GML file
nx.write_gml(G, f"{Base}/{output_file_gml}")

# Plot and save the graph as a PNG image
plt.figure(figsize=(25, 25))
pos = nx.spring_layout(G, seed=42)  # Using spring layout for better visualization
nx.draw_networkx_nodes(G, pos, node_color='k', node_size=10, alpha=0.8)
nx.draw_networkx_edges(G, pos, edge_color='r', arrows=False, style='dashed')
nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif', font_color='b')
plt.axis('off')
plt.savefig(f"{Base}/{output_file_png}", dpi=600)
plt.show()

print("### Done!! ###")
