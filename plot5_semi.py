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

# --- Scatter Plot (Y-axis log scale) ---
def plot_delta_scatter(df, mask, label, fname):
    sub = df[mask].dropna(subset=["delta5"])
    if sub.empty:
        return
    sub = sub[sub["hindex"] > 0]   # avoid meaningless hindex=0

    plt.figure(figsize=(6,4))
    plt.scatter(sub["hindex"], sub["delta5"], alpha=0.4, s=10)
    plt.yscale("symlog")   # <<<<<< log scale on Y-axis (symmetric for ±Δ)
    plt.xlabel("h-index")
    plt.ylabel("Δ = y − x (symlog scale)")
    plt.title(f"Plot 5 (Y-axis Log Scale): {label}")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.axhline(0, color="red", linestyle="--", linewidth=1)  # reference line at Δ=0
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.savefig(os.path.join(RESULTS_DIR, fname), dpi=300)
    plt.close()

# --- Combined + Categories ---
plot_delta_scatter(df, df.hindex>=0, "All Authors", "plot5_all_ylog.png")
plot_delta_scatter(df, df["soc"]==1, "Sociology Authors", "plot5_sociology_ylog.png")
plot_delta_scatter(df, df["bio"]==1, "Biology Authors", "plot5_biology_ylog.png")
plot_delta_scatter(df, df["cs"]==1, "Computer Science Authors", "plot5_cs_ylog.png")
plot_delta_scatter(df, df["title"]==3, "Professors", "plot5_prof_ylog.png")
plot_delta_scatter(df, df["title"]==2, "Postdocs", "plot5_post_ylog.png")
plot_delta_scatter(df, df["title"]==1, "Students", "plot5_students_ylog.png")
