import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

def create_network_visualization():
    # Create empty network
    G = nx.Graph()
    
    def add_relationships(file_path, type1, type2):
        with open(file_path, 'r') as f:
            next(f, None)
            for line in f:
                if not line.strip() or line.strip().isdigit():
                    continue
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    node1, node2 = parts
                    G.add_node(node1, type=type1)
                    G.add_node(node2, type=type2)
                    G.add_edge(node1, node2, type=f"{type1}-{type2}")

    # Read all relationships
    add_relationships('circRNA mRNA.txt', 'circRNA', 'mRNA')
    add_relationships('miRNA mRNA.txt', 'miRNA', 'mRNA')
    add_relationships('circRNA miRNA.txt', 'circRNA', 'miRNA')

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 15))

    # Node styling
    node_shapes = {
        'mRNA': 'o',
        'circRNA': 'o',
        'miRNA': 'o'
    }
    
    node_colors = {
        'mRNA': '#FFA500',     # Orange
        'circRNA': '#00A0FF',  # Blue
        'miRNA': '#90EE90'     # Light green
    }
    
    node_sizes = {
        'mRNA': 300,
        'circRNA': 1000,  # Larger size for circRNA
        'miRNA': 300
    }

    # First subplot - Complete network
    pos1 = nx.spring_layout(G, k=1, iterations=50)
    
    # Draw edges with different colors based on type
    edge_colors = {
        'circRNA-mRNA': '#ADD8E6',   # Light blue
        'mRNA-circRNA': '#ADD8E6',   # Light blue
        'miRNA-mRNA': '#FFB6C1',     # Light pink
        'mRNA-miRNA': '#FFB6C1',     # Light pink
        'circRNA-miRNA': '#98FB98',  # Light green
        'miRNA-circRNA': '#98FB98'   # Light green
    }

    # Draw edges by type
    for edge_type, color in edge_colors.items():
        edges = [(u, v) for (u, v, d) in G.edges(data=True) if d['type'] == edge_type]
        nx.draw_networkx_edges(G, pos1, edgelist=edges, edge_color=color, alpha=0.4, width=0.5, ax=ax1)

    # Draw nodes for each type
    for ntype in ['mRNA', 'circRNA', 'miRNA']:
        nodes = [node for node in G.nodes() if G.nodes[node]['type'] == ntype]
        nx.draw_networkx_nodes(G, pos1,
                             nodelist=nodes,
                             node_color=node_colors[ntype],
                             node_shape=node_shapes[ntype],
                             node_size=node_sizes[ntype],
                             alpha=0.7,
                             label=ntype,
                             ax=ax1)

    ax1.set_title("Complete RNA Interaction Network", pad=20, size=16)
    
    # Create custom legend
    legend_elements = [
        Patch(facecolor=node_colors['circRNA'], label='circRNA', alpha=0.7),
        Patch(facecolor=node_colors['miRNA'], label='miRNA', alpha=0.7),
        Patch(facecolor=node_colors['mRNA'], label='mRNA', alpha=0.7),
        Patch(facecolor=edge_colors['circRNA-mRNA'], label='circRNA-mRNA interaction', alpha=0.4),
        Patch(facecolor=edge_colors['miRNA-mRNA'], label='miRNA-mRNA interaction', alpha=0.4),
        Patch(facecolor=edge_colors['circRNA-miRNA'], label='circRNA-miRNA interaction', alpha=0.4)
    ]
    ax1.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.axis('off')

    # Second subplot - circRNA-centric view
    # Create subgraph centered around circRNAs
    circRNA_nodes = [node for node in G.nodes() if G.nodes[node]['type'] == 'circRNA']
    circRNA_neighbors = []
    for node in circRNA_nodes:
        circRNA_neighbors.extend(list(G.neighbors(node)))
    
    nodes_of_interest = list(set(circRNA_nodes + circRNA_neighbors))
    subgraph = G.subgraph(nodes_of_interest)
    
    pos2 = nx.spring_layout(subgraph, k=1.5, iterations=50)

    # Draw edges in subgraph
    for edge_type, color in edge_colors.items():
        edges = [(u, v) for (u, v, d) in subgraph.edges(data=True) if d['type'] == edge_type]
        nx.draw_networkx_edges(subgraph, pos2, edgelist=edges, edge_color=color, alpha=0.6, width=1.0, ax=ax2)

    # Draw nodes in subgraph
    for ntype in ['mRNA', 'circRNA', 'miRNA']:
        nodes = [node for node in subgraph.nodes() if subgraph.nodes[node]['type'] == ntype]
        nx.draw_networkx_nodes(subgraph, pos2,
                             nodelist=nodes,
                             node_color=node_colors[ntype],
                             node_shape=node_shapes[ntype],
                             node_size=node_sizes[ntype] * 1.5,  # Larger nodes in subgraph
                             alpha=0.8,
                             label=ntype,
                             ax=ax2)

    # Add labels for circRNAs
    labels = {node: node for node in subgraph.nodes() if subgraph.nodes[node]['type'] == 'circRNA'}
    nx.draw_networkx_labels(subgraph, pos2, labels, font_size=8, ax=ax2)

    ax2.set_title("circRNA-Centric Network View", pad=20, size=16)
    ax2.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.axis('off')

    plt.tight_layout()
    plt.savefig('network_with_circrna_focus.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Print network statistics
    print(f"\nNetwork Statistics:")
    print(f"Total nodes: {G.number_of_nodes()}")
    print(f"Total edges: {G.number_of_edges()}")
    for ntype in ['mRNA', 'circRNA', 'miRNA']:
        count = len([n for n in G.nodes() if G.nodes[n]['type'] == ntype])
        print(f"{ntype} nodes: {count}")

if __name__ == "__main__":
    create_network_visualization()