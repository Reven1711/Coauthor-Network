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

# Compute δh (max neighbor h − my h)
delta_h = {}
for node in G.nodes():
    nbrs = [n for n in G.neighbors(node) if n in hindex_dict]
    if nbrs:
        max_h = max(hindex_dict[n] for n in nbrs)
        delta_h[node] = max_h - hindex_dict.get(node, 0)
df["delta_h"] = df["node"].map(delta_h)

# --- Plot function ---
def plot_delta_h(df, mask, label, fname):
    sub = df[mask].dropna(subset=["delta_h"])
    plt.figure(figsize=(6,4))
    plt.scatter(sub["hindex"], sub["delta_h"], s=5, alpha=0.5)
    plt.xlabel("My h-index")
    plt.ylabel("δh = max(neighbor h) − my h")
    plt.title(f"Plot 3: {label}")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.savefig(os.path.join(RESULTS_DIR, fname), dpi=300)
    plt.close()

# --- Combined + Categories ---
plot_delta_h(df, df.hindex>=0, "All Authors", "plot3_all.png")
plot_delta_h(df, df["soc"]==1, "Sociology Authors", "plot3_sociology.png")
plot_delta_h(df, df["bio"]==1, "Biology Authors", "plot3_biology.png")
plot_delta_h(df, df["cs"]==1, "Computer Science Authors", "plot3_cs.png")
plot_delta_h(df, df["title"]==3, "Professors", "plot3_prof.png")
plot_delta_h(df, df["title"]==2, "Postdocs", "plot3_post.png")
plot_delta_h(df, df["title"]==1, "Students", "plot3_students.png")
