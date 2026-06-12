import os
import fitz
from PIL import Image

OUT = r"C:\Users\chica\Claude Skills\balanoff-law\assets\extracted"
ASSETS = r"C:\Users\chica\Claude Skills\balanoff-law\assets"
PDF = r"C:\Users\chica\OneDrive\Pictures\Camera Roll\Balanoff_20LAw_20-_20Doorhanger_20(4.25_20x_2011)_20with_20Bleed.pdf.pdf"

# Render bottom band of page 2 at 1200 dpi for max sharpness
doc = fitz.open(PDF)
page = doc[1]
r = page.rect  # 342 x 828 pt
clip = fitz.Rect(0, r.height * 0.84, r.width, r.height)
pix = page.get_pixmap(dpi=1200, clip=clip)
src_path = os.path.join(OUT, "logo_band_1200.png")
pix.save(src_path)

img = Image.open(src_path).convert("RGB")
w, h = img.size
print("band size:", img.size)

px = img.load()
bg = px[10, h // 2]  # sample the light background from the left edge mid-height
print("bg sample:", bg)

# Build RGBA: background -> transparent
rgba = Image.new("RGBA", (w, h))
dst = rgba.load()
tol = 18
minx, miny, maxx, maxy = w, h, 0, 0
for y in range(h):
    for x in range(w):
        p = px[x, y]
        if abs(p[0]-bg[0]) <= tol and abs(p[1]-bg[1]) <= tol and abs(p[2]-bg[2]) <= tol:
            dst[x, y] = (255, 255, 255, 0)
        else:
            dst[x, y] = (p[0], p[1], p[2], 255)
            if x < minx: minx = x
            if x > maxx: maxx = x
            if y < miny: miny = y
            if y > maxy: maxy = y

print("content bbox:", minx, miny, maxx, maxy)
rgba.save(os.path.join(OUT, "logo_band_alpha.png"))
