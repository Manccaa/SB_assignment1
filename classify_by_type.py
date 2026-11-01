types = dict(line.split() for line in open("types.txt"))

pairs = []
for line in open("scores.txt"):
    a, b, s = line.split()
    pairs.append((a, b, int(s)))

def subject(name):
    return name.split("_")[0]

def accuracy(threshold, use_types):
    correct = 0
    for a, b, s in pairs:
        same_subject = subject(a) == subject(b)
        if use_types and types[a] != types[b]:
            predicted_same = False          # različna tipa: ne primerjamo
        else:
            predicted_same = s >= threshold
        correct += (predicted_same == same_subject)
    return correct / len(pairs)

T = 26   # prag iz prejšnjega eksperimenta

print(f"Brez tipov (prag {T}):  {accuracy(T, False):.4f}")
print(f"S tipi     (prag {T}):  {accuracy(T, True):.4f}")

# statistika
skipped = [(a, b) for a, b, s in pairs if types[a] != types[b]]
lost_genuine = [(a, b) for a, b in skipped if subject(a) == subject(b)]
print("Parov z različnima tipoma (ne primerjamo):", len(skipped))
print("  od tega genuine parov (izgubljeni):", len(lost_genuine))

# najboljši prag za varianto s tipi
best_t = max(range(0, 251), key=lambda t: accuracy(t, True))
print(f"Najboljši prag s tipi: {best_t}, natančnost: {accuracy(best_t, True):.4f}")