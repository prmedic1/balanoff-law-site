import os
from collections import deque
from PIL import Image

OUT = r"C:\Users\chica\Claude Skills\balanoff-law\assets\extracted"
ASSETS = r"C:\Users\chica\Claude Skills\balanoff-law\assets"

img = Image.open(os.path.join(OUT, "logo_band_1200.png")).convert("RGB")
# crop to logo block only (estimated from preview, scale 7.125x)
crop = img.crop((480, 290, 4960, 1870))
w, h = crop.size
px = crop.load()
bg = (232, 234, 244)
tol = 30

def is_bg(p):
    return abs(p[0]-bg[0]) <= tol and abs(p[1]-bg[1]) <= tol and abs(p[2]-bg[2]) <= tol

# flood fill from borders
mask = bytearray(w * h)  # 1 = transparent
q = deque()
for x in range(w):
    for y in (0, h-1):
        if is_bg(px[x, y]) and not mask[y*w+x]:
            mask[y*w+x] = 1; q.append((x, y))
for y in range(h):
    for x in (0, w-1):
        if is_bg(px[x, y]) and not mask[y*w+x]:
            mask[y*w+x] = 1; q.append((x, y))
while q:
    x, y = q.popleft()
    for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        if 0 <= nx < w and 0 <= ny < h and not mask[ny*w+nx] and is_bg(px[nx, ny]):
            mask[ny*w+nx] = 1
            q.append((nx, ny))

rgba = crop.convert("RGBA")
dst = rgba.load()
minx, miny, maxx, maxy = w, h, 0, 0
for y in range(h):
    for x in range(w):
        if mask[y*w+x]:
            dst[x, y] = (255, 255, 255, 0)
        else:
            if x < minx: minx = x
            if x > maxx: maxx = x
            if y < miny: miny = y
            if y > maxy: maxy = y

trimmed = rgba.crop((minx, miny, maxx+1, maxy+1))
trimmed.save(os.path.join(ASSETS, "logo-full.png"))
print("logo size:", trimmed.size)

# preview on green
prev = trimmed.copy(); prev.thumbnail((800, 800))
bgim = Image.new("RGB", prev.size, (40, 180, 40))
bgim.paste(prev, mask=prev.split()[3])
bgim.save(os.path.join(OUT, "logo_preview.png"))

# sample brand colors from full-res page renders
page2 = Image.open(os.path.join(OUT, "hires_p2.png")).convert("RGB")
W, H = page2.size
samples = {
    "navy_text": trimmed.convert("RGB").getpixel((int(trimmed.size[0]*0.6), int(trimmed.size[1]*0.18))),
    "footer_bar": page2.getpixel((W//2, H-30)),
    "light_bg": (232, 234, 244),
}
# red star: scan shield area for most saturated red
best = None
rgb = trimmed.convert("RGB")
a = trimmed.split()[3]
for y in range(0, trimmed.size[1], 8):
    for x in range(0, int(trimmed.size[0]*0.35), 8):
        if a.getpixel((x, y)) > 200:
            r, g, b = rgb.getpixel((x, y))
            if r > 140 and r - max(g, b) > 60:
                score = r - (g + b) / 2
                if best is None or score > best[0]:
                    best = (score, (r, g, b))
samples["star_red"] = best[1] if best else None
# shield blue stripe
bestb = None
for y in range(0, trimmed.size[1], 8):
    for x in range(0, int(trimmed.size[0]*0.35), 8):
        if a.getpixel((x, y)) > 200:
            r, g, b = rgb.getpixel((x, y))
            if b > 120 and b - r > 40:
                score = b - (r + g) / 2
                if bestb is None or score > bestb[0]:
                    bestb = (score, (r, g, b))
samples["shield_blue"] = bestb[1] if bestb else None

for k, v in samples.items():
    print(k, v, "#%02x%02x%02x" % v if v else "")
