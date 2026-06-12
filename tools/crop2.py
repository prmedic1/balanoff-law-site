import os
from PIL import Image

OUT = r"C:\Users\chica\Claude Skills\balanoff-law\assets\extracted"

p1 = Image.open(os.path.join(OUT, "hires_p1.png"))
w, h = p1.size
# generous crop around the logo block on page 1 (white background)
crop1 = p1.crop((0, int(h*0.30), int(w*0.80), int(h*0.46)))
crop1.save(os.path.join(OUT, "logo_p1_crop.png"))

p2 = Image.open(os.path.join(OUT, "hires_p2.png"))
crop2 = p2.crop((0, int(h*0.85), w, h))
crop2.save(os.path.join(OUT, "logo_p2_crop.png"))
print("saved", crop1.size, crop2.size)
