import os
from collections import Counter
from PIL import Image

ASSETS = r"C:\Users\chica\Claude Skills\balanoff-law\assets"
OUT = os.path.join(ASSETS, "extracted")

logo = Image.open(os.path.join(ASSETS, "logo-full.png"))
rgb = logo.convert("RGB")
alpha = logo.split()[3]
w, h = logo.size

counts = Counter()
for y in range(0, h, 4):
    for x in range(0, w, 4):
        if alpha.getpixel((x, y)) == 255:
            r, g, b = rgb.getpixel((x, y))
            counts[(r//8*8, g//8*8, b//8*8)] += 1

print("top logo colors:")
for c, n in counts.most_common(8):
    print("#%02x%02x%02x" % c, n)

# page 1 footer bar (dark navy) and other accents
p1 = Image.open(os.path.join(OUT, "hires_p1.png")).convert("RGB")
W, H = p1.size
print("p1 footer:", "#%02x%02x%02x" % p1.getpixel((W//2, int(H*0.985))))
print("p1 deep band:", "#%02x%02x%02x" % p1.getpixel((W//2, int(H*0.93))))
p2 = Image.open(os.path.join(OUT, "hires_p2.png")).convert("RGB")
print("p2 mid band:", "#%02x%02x%02x" % p2.getpixel((W//2, int(H*0.45))))
print("p2 top:", "#%02x%02x%02x" % p2.getpixel((W//2, int(H*0.02))))
