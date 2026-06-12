import fitz, os
from PIL import Image

PDF = r"C:\Users\chica\OneDrive\Pictures\Camera Roll\Balanoff_20LAw_20-_20Doorhanger_20(4.25_20x_2011)_20with_20Bleed.pdf.pdf"
OUT = r"C:\Users\chica\Claude Skills\balanoff-law\assets\extracted"

doc = fitz.open(PDF)
for i in (0, 1):
    page = doc[i]
    pix = page.get_pixmap(dpi=600)
    pix.save(os.path.join(OUT, f"hires_p{i+1}.png"))
    print(f"page {i+1}: {pix.width}x{pix.height}, rect={page.rect}")
