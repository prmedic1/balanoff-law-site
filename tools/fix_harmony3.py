"""Redo the van removal so the corner looks natural:
1. re-crop the original to the residential ratio
2. fill the van area with plain brick cloned from the pillar (no window sills)
3. add a sidewalk band at the bottom
4. clone the real '364' glass door into the wall so the corner reads as a doorway
"""
from PIL import Image

SRC = r"C:\Users\chica\OneDrive\Pictures\Camera Roll\Harmony Hamburgers 2.JPG"
OUT = r"C:\Users\chica\Claude Skills\balanoff-law\assets\img\harmony-hamburgers-v2.jpg"
DBG = r"C:\Users\chica\Claude Skills\balanoff-law\assets\extracted"

img = Image.open(SRC).convert("RGB")
img = img.crop((0, 36, 1600, 36 + 1112))   # same ratio crop as before (1600x1112)
w, h = img.size

def hfeather(tile, fade=10):
    """alpha mask fading the left edge of a tile for horizontal blending"""
    m = Image.new("L", tile.size, 255)
    mp = m.load()
    for x in range(fade):
        a = int(255 * x / fade)
        for y in range(tile.size[1]):
            mp[x, y] = a
    return m

# --- 1. plain brick wall over the van area (x 0..248, y 700..1112) ---
WALL_TOP, WALL_BOT = 696, h
donor = img.crop((250, WALL_TOP, 330, WALL_BOT))   # clean pillar strip, no sills
donor_m = donor.transpose(Image.FLIP_LEFT_RIGHT)
wall = Image.new("RGB", (248, WALL_BOT - WALL_TOP))
for i, px in enumerate(range(0, 248, 74)):        # 80px tiles, 6px overlap
    tile = donor_m if i % 2 else donor
    wall.paste(tile, (px, 0), hfeather(tile) if px else None)
img.paste(wall, (0, WALL_TOP))

# --- 2. sidewalk band at the bottom of the filled area ---
side = img.crop((1010, 1058, 1258, h))             # sidewalk near the real door
img.paste(side, (0, 1058))

# --- 3. clone the real glass door into the wall ---
door = img.crop((858, 560, 1002, 1062))            # '364' door incl. frame
mask = Image.new("L", door.size, 255)
mp = mask.load()
F = 8
for yy in range(door.size[1]):
    for xx in range(door.size[0]):
        e = min(xx, door.size[0] - 1 - xx, yy, door.size[1] - 1 - yy)
        if e < F:
            mp[xx, yy] = int(255 * e / F)
img.paste(door, (52, 560), mask)

img.save(OUT, quality=92)
print("saved", img.size)

# previews
img.crop((0, 480, 460, h)).save(DBG + r"\h3_corner.png")
small = img.copy(); small.thumbnail((720, 720)); small.save(DBG + r"\h3_full.png")
