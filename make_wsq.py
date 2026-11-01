import subprocess
from pathlib import Path
from PIL import Image

png_dir = Path("dataset_png")
wsq_dir = Path("wsq")
wsq_dir.mkdir(exist_ok=True)

names = []
cmds = []
for png in sorted(png_dir.glob("*.png")):   #pretvori v gray in poveca
    img = Image.open(png).convert("L").resize((600, 600), Image.BICUBIC)
    (wsq_dir / f"{png.stem}.gray").write_bytes(img.tobytes())
    cmds.append(f"cwsq 0.75 wsq wsq/{png.stem}.gray -raw_in 600,600,8,500") 
    names.append(png.stem)

Path("wsq_commands.sh").write_text("\n".join(cmds) + "\n", newline="\n") #file z ukazi, ki iz gray slike naredi wsq sliko

subprocess.run(
    ["docker", "run", "--rm", "-v", f"{Path.cwd()}:/workspace",
     "zigaemersicfri/nbis:latest", "bash", "wsq_commands.sh"],
    check=True,
)

# seznam slik za pcasys, vsaka vrstica: pot + črka A
with open("paths_to_your_fingerprints_for_pcasys.txt", "w", newline="\n") as f:
    for n in names:
        f.write(f"/workspace/wsq/{n}.wsq A\n")

print("Narejenih WSQ slik:", len(names))