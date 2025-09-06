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

# Compute Δ again (same as plot 5)
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

# --- Plot 6 function ---
def plot_delta_sign_counts(df, mask, label, fname):
    sub = df[mask].dropna(subset=["delta5"])
    if sub.empty:
        return
    grouped = sub.groupby("hindex")["delta5"]

    # Count positives and negatives per h-index
    pos_counts = grouped.apply(lambda x: (x > 0).sum())
    neg_counts = grouped.apply(lambda x: (x < 0).sum())

    plt.figure(figsize=(7,5))
    plt.plot(pos_counts.index, pos_counts.values, marker="o", linestyle="-", label="Δ > 0 (positive)")
    plt.plot(neg_counts.index, neg_counts.values, marker="s", linestyle="--", label="Δ < 0 (negative)")
    plt.xlabel("h-index")
    plt.ylabel("Count of authors")
    plt.title(f"Plot 6: Δ sign counts vs h-index ({label})")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.savefig(os.path.join(RESULTS_DIR, fname), dpi=300)
    plt.close()

# --- Combined + Categories ---
plot_delta_sign_counts(df, df.hindex>=0, "All Authors", "plot6_all.png")
plot_delta_sign_counts(df, df["soc"]==1, "Sociology Authors", "plot6_sociology.png")
plot_delta_sign_counts(df, df["bio"]==1, "Biology Authors", "plot6_biology.png")
plot_delta_sign_counts(df, df["cs"]==1, "Computer Science Authors", "plot6_cs.png")
plot_delta_sign_counts(df, df["title"]==3, "Professors", "plot6_prof.png")
plot_delta_sign_counts(df, df["title"]==2, "Postdocs", "plot6_post.png")
plot_delta_sign_counts(df, df["title"]==1, "Students", "plot6_students.png")
