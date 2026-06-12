"""Make remaining lavender-background pixels (e.g. the counter of the 'O'
in ATTORNEY) transparent, while preserving the white shield interior."""
import os
from PIL import Image

PATH = r"C:\Users\chica\Claude Skills\balanoff-law\assets\logo-full.png"
OUT = r"C:\Users\chica\Claude Skills\balanoff-law\assets\extracted"

img = Image.open(PATH).convert("RGBA")
px = img.load()
w, h = img.size
bg = (232, 234, 244)
tol = 8  # tight: lavender bg yes, white shield (248,248,248) no

changed = 0
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a > 0 and abs(r-bg[0]) <= tol and abs(g-bg[1]) <= tol and abs(b-bg[2]) <= tol:
            px[x, y] = (255, 255, 255, 0)
            changed += 1

img.save(PATH)
print("pixels cleared:", changed)

# preview of the wordmark area on green to verify
prev = img.crop((int(w*0.30), int(h*0.55), w, h)).copy()
prev.thumbnail((900, 900))
bgim = Image.new("RGB", prev.size, (40, 180, 40))
bgim.paste(prev, mask=prev.split()[3])
bgim.save(os.path.join(OUT, "counter_fix_preview.png"))
