import fitz, os

PDF = r"C:\Users\chica\OneDrive\Pictures\Camera Roll\Balanoff_20LAw_20-_20Doorhanger_20(4.25_20x_2011)_20with_20Bleed.pdf.pdf"
OUT = r"C:\Users\chica\Claude Skills\balanoff-law\assets\extracted"
os.makedirs(OUT, exist_ok=True)

doc = fitz.open(PDF)
print("pages:", len(doc))
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    pix.save(os.path.join(OUT, f"page_{i+1}.png"))
    for j, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        info = doc.extract_image(xref)
        path = os.path.join(OUT, f"p{i+1}_img{j}_{xref}.{info['ext']}")
        with open(path, "wb") as f:
            f.write(info["image"])
        print(f"page {i+1} img {j}: xref={xref} {info['width']}x{info['height']} .{info['ext']}")
