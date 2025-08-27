import pandas as pd
import matplotlib.pyplot as plt

# ==== Paths ====
GS_INFO_PATH = r"gs_info.txt"

# Load gs_info
cols = ["id","cit","h","g","title","cs","bio","soc"]
df = pd.read_csv(GS_INFO_PATH, sep=" ", names=cols)

# Plot: combined distribution
plt.figure(figsize=(8,6))
df["h"].plot(kind="hist", bins=50, rwidth=0.8)
plt.xlabel("h-index")
plt.ylabel("Number of people")
plt.title("Distribution of h-index (All)")
plt.savefig("plot1_all.png", dpi=200)
plt.close()

# Subject-based distributions
for label,mask in {
    "CS": df["cs"]==1,
    "Bio": df["bio"]==1,
    "Soc": df["soc"]==1,
    "Prof": df["title"]==3,
    "Postdoc": df["title"]==2,
    "Student": df["title"]==1,
}.items():
    plt.figure(figsize=(8,6))
    df.loc[mask,"h"].plot(kind="hist", bins=50, rwidth=0.8)
    plt.xlabel("h-index")
    plt.ylabel("Number of people")
    plt.title(f"Distribution of h-index ({label})")
    plt.savefig(f"plot1_{label}.png", dpi=200)
    plt.close()
