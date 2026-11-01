from pathlib import Path
from PIL import Image

input_dir = Path("database")
output_dir = Path("dataset_png")
output_dir.mkdir(exist_ok=True)

count = 0
for tif_path in sorted(input_dir.rglob("*.tif")):
    img = Image.open(tif_path).convert("L")  # "L" = sivinska slika
    img.save(output_dir / (tif_path.stem + ".png"))
    count += 1

print("Pretvorjenih slik:", count)