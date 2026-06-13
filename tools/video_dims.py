"""Minimal MP4/MOV parser: find each track's tkhd atom and read display
width/height plus the rotation matrix, to decide portrait vs landscape."""
import struct, glob, os

def parse(path):
    size = os.path.getsize(path)
    res = []
    with open(path, "rb") as f:
        def walk(start, end):
            f.seek(start)
            while f.tell() < end:
                pos = f.tell()
                hdr = f.read(8)
                if len(hdr) < 8:
                    break
                box_size, box_type = struct.unpack(">I4s", hdr)
                if box_size == 1:
                    box_size = struct.unpack(">Q", f.read(8))[0]
                    head = 16
                else:
                    head = 8
                if box_size == 0:
                    box_size = end - pos
                if box_type in (b"moov", b"trak", b"mdia"):
                    walk(pos + head, pos + box_size)
                elif box_type == b"tkhd":
                    data = f.read(box_size - head)
                    # version(1) flags(3); v0 fields then matrix(36) + w,h(8) at tail
                    matrix = struct.unpack(">9i", data[-44:-8])
                    w = struct.unpack(">I", data[-8:-4])[0] >> 16
                    h = struct.unpack(">I", data[-4:],)[0] >> 16
                    a, b_, c, d = matrix[0], matrix[1], matrix[3], matrix[4]
                    rotated = (a == 0 and d == 0 and b_ != 0)  # 90/270 deg
                    if w and h:
                        dw, dh = (h, w) if rotated else (w, h)
                        res.append((dw, dh))
                f.seek(pos + box_size)
        walk(0, size)
    return res

for p in sorted(glob.glob(r"C:\Users\chica\OneDrive\Pictures\Camera Roll\*")):
    ext = p.lower().rsplit(".", 1)[-1]
    if ext in ("mov", "mp4", "m4v"):
        dims = [d for d in parse(p) if d[0] > 1]
        name = os.path.basename(p)
        if dims:
            w, h = max(dims, key=lambda d: d[0] * d[1])
            print(f"{name}: {w}x{h} {'portrait' if h > w else 'landscape'}")
        else:
            print(f"{name}: ?")
