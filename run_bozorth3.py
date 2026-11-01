import subprocess
from pathlib import Path
from itertools import combinations

names = sorted(p.stem for p in Path("out").glob("*.xyt"))
print("Število odtisov:", len(names))

# shell skripta, ki se izvede znotraj containerja
lines = []
for a, b in combinations(names, 2):
    lines.append(f"echo {a} {b} $(bozorth3 out/{a}.xyt out/{b}.xyt)")
Path("bozorth_commands.sh").write_text("\n".join(lines) + "\n", newline="\n")

# zaženemo container enkrat in mu damo to skripto
result = subprocess.run(
    ["docker", "run", "--rm", "-v", f"{Path.cwd()}:/workspace",
     "zigaemersicfri/nbis:latest", "bash", "bozorth_commands.sh"],
    capture_output=True, text=True, check=True,
)
Path("scores.txt").write_text(result.stdout)
print("Shranjeno v scores.txt, vrstic:", len(result.stdout.splitlines()))