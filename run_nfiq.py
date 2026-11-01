import subprocess
from pathlib import Path

pngs = sorted(Path("dataset_png").glob("*.png"))

lines = [f"echo {p.stem} $(nfiq dataset_png/{p.name})" for p in pngs]
Path("nfiq_commands.sh").write_text("\n".join(lines) + "\n", newline="\n")

result = subprocess.run(
    ["docker", "run", "--rm", "-v", f"{Path.cwd()}:/workspace",
     "zigaemersicfri/nbis:latest", "bash", "nfiq_commands.sh"],
    capture_output=True, text=True, check=True,
)
Path("quality.txt").write_text(result.stdout)
print("Shranjeno v quality.txt, vrstic:", len(result.stdout.splitlines()))