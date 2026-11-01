import matplotlib.pyplot as plt
from collections import Counter

names, quals = [], []
for line in open("quality.txt"):
    name, q = line.split()
    names.append(name)
    quals.append(int(q))

# 1. stolpčni graf: koliko odtisov ima katero kakovost
counts = Counter(quals)
levels = [1, 2, 3, 4, 5]
values = [counts.get(l, 0) for l in levels]

plt.figure(figsize=(6, 4))
plt.bar(levels, values, color="tab:blue")
plt.xlabel("NFIQ kakovost (1 = najboljša, 5 = najslabša)")
plt.ylabel("Število odtisov")
plt.xticks(levels)
plt.tight_layout()
plt.savefig("plot_quality.png", dpi=200)

# 2. povprečna kakovost po prstih
fingers = sorted({n.split("_")[0] for n in names})
for f in fingers:
    q = [quals[i] for i, n in enumerate(names) if n.startswith(f + "_")]
    print(f, "povprečna kakovost:", round(sum(q) / len(q), 2))

plt.show()