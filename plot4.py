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

# Compute δℓ (my h − min neighbor h)
delta_l = {}
for node in G.nodes():
    nbrs = [n for n in G.neighbors(node) if n in hindex_dict]
    if nbrs:
        min_h = min(hindex_dict[n] for n in nbrs)
        delta_l[node] = hindex_dict.get(node, 0) - min_h
df["delta_l"] = df["node"].map(delta_l)

# --- Plot function ---
def plot_delta_l(df, mask, label, fname):
    sub = df[mask].dropna(subset=["delta_l"])
    plt.figure(figsize=(6,4))
    plt.scatter(sub["hindex"], sub["delta_l"], s=5, alpha=0.5)
    plt.xlabel("My h-index")
    plt.ylabel("δℓ = my h − min(neighbor h)")
    plt.title(f"Plot 4: {label}")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.savefig(os.path.join(RESULTS_DIR, fname), dpi=300)
    plt.close()

# --- Combined + Categories ---
plot_delta_l(df, df.hindex>=0, "All Authors", "plot4_all.png")
plot_delta_l(df, df["soc"]==1, "Sociology Authors", "plot4_sociology.png")
plot_delta_l(df, df["bio"]==1, "Biology Authors", "plot4_biology.png")
plot_delta_l(df, df["cs"]==1, "Computer Science Authors", "plot4_cs.png")
plot_delta_l(df, df["title"]==3, "Professors", "plot4_prof.png")
plot_delta_l(df, df["title"]==2, "Postdocs", "plot4_post.png")
plot_delta_l(df, df["title"]==1, "Students", "plot4_students.png")
