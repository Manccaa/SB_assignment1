import re
from collections import Counter

types = {}
for line in open("pcasys.out"):
    m = re.match(r"^(\d+_\d+)\.wsq:.*?nn: hyp (\w)", line)
    if m:
        types[m.group(1)] = m.group(2)

with open("types.txt", "w") as f:
    for name in sorted(types):
        f.write(f"{name} {types[name]}\n")

print("Odtisov s tipom:", len(types))
print(Counter(types.values()))