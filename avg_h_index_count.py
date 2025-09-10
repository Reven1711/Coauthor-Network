import pandas as pd
import networkx as nx
import os

# ==== HARD-CODED PATHS ====
NODES_PATH   = r"nodes.txt"
EDGES_PATH   = r"edges.txt"
GS_INFO_PATH = r"gs_info.txt"
RESULTS_DIR  = r"results"
# ===========================

# Read gs_info
cols = ["node","citations","hindex","gindex","title","cs","bio","soc"]
df = pd.read_csv(GS_INFO_PATH, sep=" ", names=cols)

# Build graph
G = nx.read_edgelist(EDGES_PATH, delimiter=",", nodetype=int)

# Fast lookup dictionary
hindex_dict = dict(zip(df["node"], df["hindex"]))

# --- Count logic ---
higher_count = 0
lower_count = 0
equal_count = 0

for node in G.nodes():
    my_h = hindex_dict.get(node, None)
    if my_h is None:
        continue

    nbrs = [n for n in G.neighbors(node) if n in hindex_dict]
    if not nbrs:
        continue

    avg_h = sum(hindex_dict[n] for n in nbrs) / len(nbrs)

    if avg_h > my_h:
        higher_count += 1
    elif avg_h < my_h:
        lower_count += 1
    else:
        equal_count += 1

# Print results
print("Number of authors where neighbors' avg h-index > author's h-index:", higher_count)
print("Number of authors where neighbors' avg h-index < author's h-index:", lower_count)
print("Number of authors where neighbors' avg h-index = author's h-index:", equal_count)

# Save results to file
os.makedirs(RESULTS_DIR, exist_ok=True)
with open(os.path.join(RESULTS_DIR, "neighbor_hindex_comparison.txt"), "w") as f:
    f.write(f"Neighbors' avg h-index > author's h-index: {higher_count}\n")
    f.write(f"Neighbors' avg h-index < author's h-index: {lower_count}\n")
    f.write(f"Neighbors' avg h-index = author's h-index: {equal_count}\n")
