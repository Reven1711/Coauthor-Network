import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain  # pip install python-louvain

# --- Step 1: Import the graph ---
gexf_file = 'coauthor_network_no_bridges.gexf'
G = nx.read_gexf(gexf_file)
print(f"Imported graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

# --- Step 2: Assign colors based on author domain ---
node_colors = {}
for node, data in G.nodes(data=True):
    cs = int(data.get('cs_author', 0))
    bio = int(data.get('biology_author', 0))
    soc = int(data.get('sociology_author', 0))

    if cs and not bio and not soc:
        color = 'blue'
    elif bio and not cs and not soc:
        color = 'green'
    elif soc and not cs and not bio:
        color = 'orange'
    elif (cs + bio + soc) > 1:
        color = 'purple'  # Multi-domain author
    else:
        color = 'gray'    # No domain assigned
    node_colors[node] = color

# Save colors as node attributes
nx.set_node_attributes(G, node_colors, "domain_color")

# --- Step 3: Apply Louvain community detection ---
partition = community_louvain.best_partition(G)
nx.set_node_attributes(G, partition, "louvain_community")

print(f"Louvain found {len(set(partition.values()))} communities.")

# --- Step 4: Optional small visualization (skip if graph is huge) ---
if G.number_of_nodes() <= 1000:
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 10))
    nx.draw_networkx_nodes(G, pos, node_color=[node_colors[n] for n in G.nodes()], node_size=50)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.title("Bridge-Free Coauthor Network (Colored by Domain)")
    plt.axis('off')
    plt.show()

# --- Step 5: Export updated graph with Louvain communities & colors ---
nx.write_gexf(G, 'coauthor_network_no_bridges_louvain.gexf')
print("Updated graph saved to coauthor_network_no_bridges_louvain.gexf with domain colors and Louvain communities.")
