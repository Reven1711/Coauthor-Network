import pandas as pd
import matplotlib.pyplot as plt
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

# Compute Δ = y - x
delta = {}
for node in G.nodes():
    my_h = hindex_dict.get(node, None)
    if my_h is None: 
        continue
    nbrs = [n for n in G.neighbors(node) if n in hindex_dict]
    if not nbrs:
        continue

    x_val = sum(hindex_dict[n] - my_h for n in nbrs if hindex_dict[n] >= my_h)
    y_val = sum(my_h - hindex_dict[n] for n in nbrs if hindex_dict[n] < my_h)
    delta[node] = y_val - x_val

df["delta5"] = df["node"].map(delta)

# --- Plot function ---
def plot_delta(df, mask, label, fname):
    sub = df[mask].dropna(subset=["delta5"])
    plt.figure(figsize=(6,4))
    plt.scatter(sub["hindex"], sub["delta5"], s=5, alpha=0.5)
    plt.xlabel("My h-index")
    plt.ylabel("Δ = y − x")
    plt.title(f"Plot 5: {label}")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.savefig(os.path.join(RESULTS_DIR, fname), dpi=300)
    plt.close()

# --- Combined + Categories ---
plot_delta(df, df.hindex>=0, "All Authors", "plot5_all.png")
plot_delta(df, df["soc"]==1, "Sociology Authors", "plot5_sociology.png")
plot_delta(df, df["bio"]==1, "Biology Authors", "plot5_biology.png")
plot_delta(df, df["cs"]==1, "Computer Science Authors", "plot5_cs.png")
plot_delta(df, df["title"]==3, "Professors", "plot5_prof.png")
plot_delta(df, df["title"]==2, "Postdocs", "plot5_post.png")
plot_delta(df, df["title"]==1, "Students", "plot5_students.png")
