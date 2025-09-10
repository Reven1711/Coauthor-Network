import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import os
from collections import Counter

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

# Compute degrees
degree_dict = dict(G.degree())
df["degree"] = df["node"].map(degree_dict)

# --- Plot 7a: Degree Distribution ---
def plot_degree_distribution(df, mask, label, fname):
    sub = df[mask].dropna(subset=["degree"])
    if sub.empty:
        return
    degree_counts = Counter(sub["degree"])
    deg_x = sorted(degree_counts.keys())
    deg_y = [degree_counts[d] for d in deg_x]

    plt.figure(figsize=(7,5))
    plt.bar(deg_x, deg_y, color="skyblue", edgecolor="black")
    plt.xlabel("Degree (number of co-authors)")
    plt.ylabel("Number of authors")
    plt.title(f"Plot 7a: Degree Distribution ({label})")
    plt.grid(True, linestyle="--", alpha=0.5)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.savefig(os.path.join(RESULTS_DIR, fname), dpi=300)
    plt.close()

# --- Plot 7b: h-index vs Degree ---
def plot_hindex_vs_degree(df, mask, label, fname):
    sub = df[mask].dropna(subset=["degree","hindex"])
    if sub.empty:
        return

    plt.figure(figsize=(7,5))
    plt.scatter(sub["hindex"], sub["degree"], alpha=0.6, edgecolors="k")
    plt.xlabel("h-index")
    plt.ylabel("Degree (number of co-authors)")
    plt.title(f"Plot 7b: h-index vs Degree ({label})")
    plt.grid(True, linestyle="--", alpha=0.5)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.savefig(os.path.join(RESULTS_DIR, fname), dpi=300)
    plt.close()

# --- Combined + Categories ---
plot_degree_distribution(df, df.hindex>=0, "All Authors", "plot7a_all.png")
plot_hindex_vs_degree(df, df.hindex>=0, "All Authors", "plot7b_all.png")

plot_degree_distribution(df, df["soc"]==1, "Sociology Authors", "plot7a_sociology.png")
plot_hindex_vs_degree(df, df["soc"]==1, "Sociology Authors", "plot7b_sociology.png")

plot_degree_distribution(df, df["bio"]==1, "Biology Authors", "plot7a_biology.png")
plot_hindex_vs_degree(df, df["bio"]==1, "Biology Authors", "plot7b_biology.png")

plot_degree_distribution(df, df["cs"]==1, "Computer Science Authors", "plot7a_cs.png")
plot_hindex_vs_degree(df, df["cs"]==1, "Computer Science Authors", "plot7b_cs.png")

plot_degree_distribution(df, df["title"]==3, "Professors", "plot7a_prof.png")
plot_hindex_vs_degree(df, df["title"]==3, "Professors", "plot7b_prof.png")

plot_degree_distribution(df, df["title"]==2, "Postdocs", "plot7a_post.png")
plot_hindex_vs_degree(df, df["title"]==2, "Postdocs", "plot7b_post.png")

plot_degree_distribution(df, df["title"]==1, "Students", "plot7a_students.png")
plot_hindex_vs_degree(df, df["title"]==1, "Students", "plot7b_students.png")
