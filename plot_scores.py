import numpy as np
import matplotlib.pyplot as plt

# 1. branje scores.txt
pairs = []
for line in open("scores.txt"):
    a, b, s = line.split()
    pairs.append((a, b, int(s)))

names = sorted({n for a, b, _ in pairs for n in (a, b)})    #po abecedi izlusci imena
index = {n: i for i, n in enumerate(names)}    #ta imena indeksira da bo lahko naredil matriko

def subject(name):    #odstrani številko za _ da lahko vidim ce je isti prst ko kasneje primerjam dva odtisa
    return name.split("_")[0]  # "101_1" -> "101"

genuine = [s for a, b, s in pairs if subject(a) == subject(b)]
impostor = [s for a, b, s in pairs if subject(a) != subject(b)]
print("Genuine:", len(genuine), " Impostor:", len(impostor))

# 2. graf genuine vs impostor
plt.figure(figsize=(7, 4))
bins = np.arange(0, max(genuine + impostor) + 5, 5) #najde max oceno da lahko naredi označitev osi
plt.hist(impostor, bins=bins, alpha=0.6, label="Impostor", color="tab:red")
plt.hist(genuine, bins=bins, alpha=0.6, label="Genuine", color="tab:green")
plt.yscale("log")
plt.xlabel("Bozorth3 ocena")
plt.ylabel("Število parov (log)")
plt.legend()
plt.tight_layout()
plt.savefig("plot_genuine_impostor.png", dpi=200)

# 3. matrika podobnosti
n = len(names)
matrix = np.zeros((n, n))
for a, b, s in pairs:
    i, j = index[a], index[b]
    matrix[i, j] = s
    matrix[j, i] = s  # simetrično, da je matrika polna

plt.figure(figsize=(6, 5))
plt.imshow(matrix, cmap="viridis")
plt.colorbar(label="Bozorth3 ocena")
plt.xlabel("Odtis")
plt.ylabel("Odtis")
plt.tight_layout()
plt.savefig("plot_similarity_matrix.png", dpi=200)

plt.show()