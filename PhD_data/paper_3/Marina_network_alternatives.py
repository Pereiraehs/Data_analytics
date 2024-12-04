import networkx as nx
import pandas as pd

def load_network_data():
    G = nx.Graph()
    
    def add_relationships(file_path, type1, type2):
        df = pd.read_csv(file_path, sep='\t')
        for _, row in df.iterrows():
            G.add_node(row.iloc[0], type=type1)
            G.add_node(row.iloc[1], type=type2)
            G.add_edge(row.iloc[0], row.iloc[1], type=f"{type1}-{type2}")
        return df
    
    circ_mrna = add_relationships('circRNA mRNA.txt', 'circRNA', 'mRNA')
    mirna_mrna = add_relationships('miRNA mRNA.txt', 'miRNA', 'mRNA')
    circ_mirna = add_relationships('circRNA miRNA.txt', 'circRNA', 'miRNA')
    
    return G, (circ_mrna, mirna_mrna, circ_mirna)

if __name__ == "__main__":
    G, (circ_mrna, mirna_mrna, circ_mirna) = load_network_data()
    print("Network data loaded successfully!")
    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Number of edges: {G.number_of_edges()}") 