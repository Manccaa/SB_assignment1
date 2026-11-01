import numpy as np
import matplotlib.pyplot as plt

pairs = []
for line in open("scores.txt"):
    a, b, s = line.split()
    pairs.append((a, b, int(s)))

def subject(name):
    return name.split("_")[0]

genuine = np.array([s for a, b, s in pairs if subject(a) == subject(b)])
impostor = np.array([s for a, b, s in pairs if subject(a) != subject(b)])
total = len(genuine) + len(impostor)

thresholds = np.arange(0, 251)
far, frr, acc = [], [], []
for t in thresholds:
    fa = np.sum(impostor >= t)   # napačno sprejeti impostorji
    fr = np.sum(genuine < t)     # napačno zavrnjeni genuine
    far.append(fa / len(impostor))
    frr.append(fr / len(genuine))
    acc.append((total - fa - fr) / total)

far, frr, acc = np.array(far), np.array(frr), np.array(acc)

# EER: točka, kjer je razlika med FAR in FRR najmanjša
i_eer = np.argmin(np.abs(far - frr))
# najboljša natančnost
i_acc = np.argmax(acc)

print(f"EER prag: {thresholds[i_eer]}, FAR={far[i_eer]:.3f}, FRR={frr[i_eer]:.3f}")
print(f"Prag z najvišjo natančnostjo: {thresholds[i_acc]}, natančnost={acc[i_acc]:.4f}")

plt.figure(figsize=(7, 4))
plt.plot(thresholds, far, label="FAR")
plt.plot(thresholds, frr, label="FRR")
plt.axvline(thresholds[i_eer], color="gray", linestyle="--", label="EER prag")
plt.xlabel("Prag")
plt.ylabel("Delež napak")
plt.legend()
plt.tight_layout()
plt.savefig("plot_far_frr.png", dpi=200)
plt.show()