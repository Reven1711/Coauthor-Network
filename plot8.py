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

# Classify each node as source, sink, or neutral
role = {}
for node in G.nodes():
    my_h = hindex_dict.get(node, None)
    if my_h is None:
        continue
    nbrs = [n for n in G.neighbors(node) if n in hindex_dict]
    if not nbrs:
        continue

    avg_h = sum(hindex_dict[n] for n in nbrs) / len(nbrs)

    if avg_h < my_h:
        role[node] = "source"
    elif avg_h > my_h:
        role[node] = "sink"
    else:
        role[node] = "neutral"

df["role"] = df["node"].map(role)

# --- Helper function ---
def plot_source_sink(df, bucket_size, fname):
    # Bucket h-index
    df = df.copy()
    if bucket_size > 1:
        df["bucket"] = (df["hindex"] // bucket_size) * bucket_size
    else:
        df["bucket"] = df["hindex"]

    grouped = df.groupby("bucket")["role"]

    pct_source = grouped.apply(lambda x: (x=="source").sum() / len(x) * 100)
    pct_sink   = grouped.apply(lambda x: (x=="sink").sum() / len(x) * 100)

    # Keep only X <= 50
    pct_source = pct_source[pct_source.index <= 50]
    pct_sink   = pct_sink[pct_sink.index <= 50]

    plt.figure(figsize=(9,6))
    plt.plot(pct_source.index, pct_source.values, marker="o", label="% Source")
    plt.plot(pct_sink.index, pct_sink.values, marker="s", label="% Sink")

    # --- Add labels on nodes ---
    for x, y in zip(pct_source.index, pct_source.values):
        plt.text(x, y+0.5, f"{y:.1f}%", fontsize=8, ha="center", color="blue")
    for x, y in zip(pct_sink.index, pct_sink.values):
        plt.text(x, y-2, f"{y:.1f}%", fontsize=8, ha="center", color="green")

    plt.xlabel("h-index (bucket size = %d)" % bucket_size)
    plt.ylabel("Percentage of authors")
    plt.title(f"Plot 8: % of Source vs Sink (bucket={bucket_size})")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.savefig(os.path.join(RESULTS_DIR, fname), dpi=300)
    plt.close()

# --- Run for single, bucket of 3, bucket of 5 ---
plot_source_sink(df, 1,  "plot8_bucket1.png")
plot_source_sink(df, 3,  "plot8_bucket3.png")
plot_source_sink(df, 5,  "plot8_bucket5.png")

print("Plot 8 saved in results folder with labels (bucket=1,3,5)")
