import subprocess
from pathlib import Path

png_dir = Path("dataset_png")
out_dir = Path("out")
out_dir.mkdir(exist_ok=True)

for png in sorted(png_dir.glob("*.png")):
    name = png.stem
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{Path.cwd()}:/workspace",
        "zigaemersicfri/nbis:latest",
        "mindtct", f"dataset_png/{png.name}", f"out/{name}",
    ]
    subprocess.run(cmd, check=True)
    print("Končano:", name)