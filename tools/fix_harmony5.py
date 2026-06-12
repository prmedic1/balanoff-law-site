"""Minimal retouch: cover only the van by extending what is directly above it
straight down, column band by column band:
  band A x 0-100    ENVIOS storefront glass/frame
  band B x 100-170  brick pillar
  band C x 170-240  the gray door panel (extends the door frame down)
then a sidewalk strip across the bottom of the patched area.
Everything outside x 0-240 / y 920-1200 is untouched."""
from PIL import Image

SRC = r"C:\Users\chica\OneDrive\Pictures\Camera Roll\Harmony Hamburgers 2.JPG"
OUT = r"C:\Users\chica\Claude Skills\balanoff-law\assets\img\harmony-hamburgers-v4.jpg"
DBG = r"C:\Users\chica\Claude Skills\balanoff-law\assets\extracted"

img = Image.open(SRC).convert("RGB")  # 1600 x 1200

def vfeather(tile, fade=14):
    m = Image.new("L", tile.size, 255)
    mp = m.load()
    for y in range(fade):
        a = int(255 * y / fade)
        for x in range(tile.size[0]):
            mp[x, y] = a
    return m

def extend_down(x1, x2, src_top, src_bot, start, end):
    tile = img.crop((x1, src_top, x2, src_bot))
    step = src_bot - src_top
    y = start
    first = True
    while y < end:
        img.paste(tile, (x1, y), None if first else vfeather(tile))
        y += step - 10
        first = False

# band A: ENVIOS storefront (a second parked car peeks in from y~845,
# so sample above it and start covering from there)
extend_down(0, 100, 686, 780, 780, 1200)
# band B: brick pillar
extend_down(100, 170, 690, 915, 915, 1200)
# band C: gray door panel
extend_down(170, 240, 780, 915, 915, 1200)

# soften the extended storefront glass so pane repetition reads as shadow
from PIL import ImageFilter, ImageEnhance
glass = img.crop((0, 790, 100, 1128))
glass = glass.filter(ImageFilter.GaussianBlur(2.2))
glass = ImageEnhance.Brightness(glass).enhance(0.9)
img.paste(glass, (0, 845), vfeather(glass, 24))

# sidewalk across the bottom of the patch
side = img.crop((245, 1128, 485, 1200))
sm = vfeather(side, 18)
img.paste(side, (0, 1128), sm)

# crop to the residential card ratio, as before
img = img.crop((0, 36, 1600, 36 + 1112))
img.save(OUT, quality=92)
print("saved", img.size)

img.crop((0, 480, 460, 1112)).save(DBG + r"\h5_corner.png")
small = img.copy(); small.thumbnail((720, 720)); small.save(DBG + r"\h5_full.png")
