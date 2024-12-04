import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Sample data - replace with your actual data
# Format: source, target, interaction_type
interactions_data = [
    ('circRNA1', 'miRNA1', 'circRNA-miRNA'),
    ('miRNA1', 'mRNA1', 'miRNA-mRNA'),
    ('circRNA2', 'miRNA2', 'circRNA-miRNA'),
    ('miRNA2', 'mRNA2', 'miRNA-mRNA'),
    # Add more interactions as needed
]

# Create a network graph
G = nx.Graph()

# Add edges with different colors based on interaction type
edge_colors = []
for source, target, interaction_type in interactions_data:
    G.add_edge(source, target)
    if interaction_type == 'circRNA-miRNA':
        edge_colors.append('red')
    else:
        edge_colors.append('blue')

# Set node colors based on RNA type
node_colors = []
for node in G.nodes():
    if 'circRNA' in node:
        node_colors.append('lightgreen')
    elif 'miRNA' in node:
        node_colors.append('lightblue')
    else:
        node_colors.append('pink')

# Create the visualization
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=1, iterations=50)

# Draw the network
nx.draw(G, pos,
        node_color=node_colors,
        edge_color=edge_colors,
        with_labels=True,
        node_size=2000,
        font_size=10,
        font_weight='bold')

# Add a legend
legend_elements = [plt.Line2D([0], [0], color='red', label='circRNA-miRNA'),
                  plt.Line2D([0], [0], color='blue', label='miRNA-mRNA'),
                  plt.scatter([0], [0], color='lightgreen', label='circRNA'),
                  plt.scatter([0], [0], color='lightblue', label='miRNA'),
                  plt.scatter([0], [0], color='pink', label='mRNA')]

plt.legend(handles=legend_elements, loc='upper right')
plt.title('circRNA-miRNA-mRNA Network')
plt.axis('off')
plt.tight_layout()
plt.show()