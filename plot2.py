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

# Compute avg h-index of neighbors (fast)
avg_h_neighbors = {
    node: (sum(hindex_dict[nbr] for nbr in G.neighbors(node) if nbr in hindex_dict) / 
           max(1, len([nbr for nbr in G.neighbors(node) if nbr in hindex_dict])))
    for node in G.nodes()
}

df["avg_h_neighbors"] = df["node"].map(avg_h_neighbors)

# --- Plot function ---
def plot_avg_h(df, mask, label, fname):
    sub = df[mask].dropna(subset=["avg_h_neighbors"])
    plt.figure(figsize=(6,4))
    plt.scatter(sub["hindex"], sub["avg_h_neighbors"], s=5, alpha=0.5)
    plt.xlabel("My h-index")
    plt.ylabel("Avg h-index of neighbors")
    plt.title(f"Plot 2: {label}")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.savefig(os.path.join(RESULTS_DIR, fname), dpi=300)
    plt.close()

# --- Combined ---
plot_avg_h(df, df.hindex>=0, "All Authors", "plot2_all.png")

# --- Categories ---
plot_avg_h(df, df["soc"]==1, "Sociology Authors", "plot2_sociology.png")
plot_avg_h(df, df["bio"]==1, "Biology Authors", "plot2_biology.png")
plot_avg_h(df, df["cs"]==1, "Computer Science Authors", "plot2_cs.png")
plot_avg_h(df, df["title"]==3, "Professors", "plot2_prof.png")
plot_avg_h(df, df["title"]==2, "Postdocs", "plot2_post.png")
plot_avg_h(df, df["title"]==1, "Students", "plot2_students.png")
