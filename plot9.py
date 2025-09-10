import os
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from community import community_louvain
from tqdm import tqdm

# ==== HARD-CODED PATHS ====
GEXF_PATH   = r"coauthor_network_no_bridges.gexf"
GS_INFO_PATH = r"gs_info.txt"
RESULTS_DIR  = r"results"
# ===========================

# --- Step 1: Load GEXF Graph ---
G = nx.read_gexf(GEXF_PATH)
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

nx.set_node_attributes(G, node_colors, "domain_color")

# --- Step 3: Louvain Community Detection ---
print("Running Louvain community detection...")
partition = community_louvain.best_partition(G)
nx.set_node_attributes(G, partition, "louvain_community")

# --- Step 4: Load GS Info for h-index ---
cols = ["node","citations","hindex","gindex","title","cs","bio","soc"]
df = pd.read_csv(GS_INFO_PATH, sep=" ", names=cols)
hindex_dict = dict(zip(df["node"].astype(str), df["hindex"]))  # ensure string IDs

# --- Step 5: Compute community max h-index ---
community_hindexes = {}
print("Computing community h-index distribution...")
for node, comm_id in tqdm(partition.items(), total=len(partition)):
    h = hindex_dict.get(str(node))
    if h is None:
        continue
    if comm_id not in community_hindexes:
        community_hindexes[comm_id] = []
    community_hindexes[comm_id].append(h)

# Get max h-index per community
community_max_h = [max(vals) for vals in community_hindexes.values() if vals]

# Sort communities by ID for consistent x-axis
community_ids = sorted(community_hindexes.keys())
max_h_values = [max(community_hindexes[c]) for c in community_ids if community_hindexes[c]]

# --- Step 6: Scatter/Line Plot ---
plt.figure(figsize=(10,6))
plt.plot(range(1, len(max_h_values)+1), max_h_values, marker="o", linestyle="-", color="teal")
plt.xlabel("Community Index")
plt.ylabel("Max h-index")
plt.title("Plot 9: Max h-index per Community")
plt.grid(True, linestyle="--", alpha=0.6)

# Save plot
os.makedirs(RESULTS_DIR, exist_ok=True)
plt.savefig(os.path.join(RESULTS_DIR, "plot9_max_hindex_per_community.png"), dpi=300)
plt.close()

print("✅ Plot 9 saved in results folder.")
