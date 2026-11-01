import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

plt.rcParams.update({
    "font.size": 8, "font.family": "serif",
    "axes.labelsize": 8, "legend.fontsize": 7,
    "pdf.fonttype": 42,
})
W, H = 3.4, 2.2   # širina enega stolpca IEEE predloge (palci)

pairs = [(a, b, int(s)) for a, b, s in (l.split() for l in open("scores.txt"))]
subject = lambda n: n.split("_")[0]
genuine = np.array([s for a, b, s in pairs if subject(a) == subject(b)])
impostor = np.array([s for a, b, s in pairs if subject(a) != subject(b)])
total = len(genuine) + len(impostor)

# 1. genuine vs impostor
plt.figure(figsize=(W, H))
bins = np.arange(0, max(genuine.max(), impostor.max()) + 5, 5)
plt.hist(impostor, bins=bins, alpha=0.6, color="tab:red", label="Impostor")
plt.hist(genuine, bins=bins, alpha=0.6, color="tab:green", label="Genuine")
plt.yscale("log")
plt.xlabel("Bozorth3 score")
plt.ylabel("Number of pairs")
plt.legend()
plt.tight_layout()
plt.savefig("plot_genuine_impostor.pdf")

# 2. matrika podobnosti
names = sorted({n for a, b, _ in pairs for n in (a, b)})
idx = {n: i for i, n in enumerate(names)}
m = np.zeros((len(names), len(names)))
for a, b, s in pairs:
    m[idx[a], idx[b]] = s
    m[idx[b], idx[a]] = s
plt.figure(figsize=(W, 2.8))
plt.imshow(m, cmap="viridis")
plt.colorbar(label="Bozorth3 score")
plt.xlabel("Fingerprint index")
plt.ylabel("Fingerprint index")
plt.tight_layout()
plt.savefig("plot_similarity_matrix.pdf")

# 3. kakovost
quals = [int(l.split()[1]) for l in open("quality.txt")]
c = Counter(quals)
plt.figure(figsize=(W, H))
plt.bar(range(1, 6), [c.get(i, 0) for i in range(1, 6)], color="tab:blue")
plt.xlabel("NFIQ quality (1 = best, 5 = worst)")
plt.ylabel("Number of images")
plt.tight_layout()
plt.savefig("plot_quality.pdf")

# 4. FAR in FRR
thr = np.arange(0, 251)
far = np.array([(impostor >= t).mean() for t in thr])
frr = np.array([(genuine < t).mean() for t in thr])
acc = 1 - (far * len(impostor) + frr * len(genuine)) / total
t_eer = thr[np.argmin(np.abs(far - frr))]
t_acc = thr[np.argmax(acc)]
print("EER prag:", t_eer, " prag z najvišjo natančnostjo:", t_acc)
i = list(thr).index(t_acc)
print(f"Pri T={t_acc}: FAR={far[i]:.4f}, FRR={frr[i]:.4f}, accuracy={acc[i]:.4f}")

plt.figure(figsize=(W, H))
plt.plot(thr, far, label="FAR")
plt.plot(thr, frr, label="FRR")
plt.axvline(t_eer, color="gray", linestyle="--", label=f"EER ($T$={t_eer})")
plt.axvline(t_acc, color="black", linestyle=":", label=f"Max. accuracy ($T$={t_acc})")
plt.xlabel("Threshold $T$")
plt.ylabel("Error rate")
plt.legend()
plt.tight_layout()
plt.savefig("plot_far_frr.pdf")
print("Grafi shranjeni kot PDF.")