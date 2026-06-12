"""Remove the van (rear window and body) from the bottom-left corner by
tiling the brick wall above it downward, then crop the photo to the same
aspect ratio as the residential card photo (640x445 = 1.438)."""
from PIL import Image

SRC = r"C:\Users\chica\OneDrive\Pictures\Camera Roll\Harmony Hamburgers 2.JPG"
OUT = r"C:\Users\chica\Claude Skills\balanoff-law\assets\img\harmony-hamburgers.jpg"

img = Image.open(SRC).convert("RGB")
w, h = img.size  # 1600 x 1200
print("source:", img.size)

# van occupies x 0..~236, y ~744..1200
PATCH_X1 = 240
DONOR_TOP, DONOR_BOT = 660, 744   # clean brick strip directly above the van
donor = img.crop((0, DONOR_TOP, PATCH_X1, DONOR_BOT))
step = DONOR_BOT - DONOR_TOP

# soft top edge so each tile blends into the previous one
mask = Image.new("L", donor.size, 255)
mp = mask.load()
for y in range(12):
    for x in range(donor.size[0]):
        mp[x, y] = int(255 * y / 12)

y = 744
while y < h:
    img.paste(donor, (0, y), mask)
    y += step - 6  # slight overlap hides seams

# crop to residential photo ratio 640/445
target_ratio = 640 / 445
new_h = round(w / target_ratio)  # 1112
top = 36                          # trim mostly from the top brick, keep the sign
img = img.crop((0, top, w, top + new_h))
img.save(OUT, quality=92)
print("saved", img.size, "ratio", round(img.size[0]/img.size[1], 3))
