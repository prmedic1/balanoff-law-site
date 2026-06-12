"""Make the old van corner a natural-looking double-door building entrance:
clone the real '364' glass door and its mirror image side by side across the
full strip, with sidewalk below. No brick tiling, no repetition artifacts."""
from PIL import Image

SRC = r"C:\Users\chica\OneDrive\Pictures\Camera Roll\Harmony Hamburgers 2.JPG"
OUT = r"C:\Users\chica\Claude Skills\balanoff-law\assets\img\harmony-hamburgers-v2.jpg"
DBG = r"C:\Users\chica\Claude Skills\balanoff-law\assets\extracted"

img = Image.open(SRC).convert("RGB")
img = img.crop((0, 36, 1600, 36 + 1112))
w, h = img.size

# real glass door incl. aluminum frame
door = img.crop((858, 560, 1002, 1062))          # 144 x 502
door_m = door.transpose(Image.FLIP_LEFT_RIGHT)

# double-door unit, 248 wide: right portion of mirrored door + left-aligned door
unit = Image.new("RGB", (248, 502))
unit.paste(door_m.crop((20, 0, 144, 502)), (0, 0))
unit.paste(door.crop((20, 0, 144, 502)), (124, 0))
img.paste(unit, (0, 560))

# sidewalk band under the doors
side = img.crop((1010, 1058, 1258, h))
img.paste(side, (0, 1058))

img.save(OUT, quality=92)
print("saved", img.size)

img.crop((0, 440, 520, h)).save(DBG + r"\h4_corner.png")
small = img.copy(); small.thumbnail((720, 720)); small.save(DBG + r"\h4_full.png")
