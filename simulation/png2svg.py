import cv2
import potrace
import numpy as np
from os import path

curr_dir = path.dirname(__file__)
PATH = path.join(curr_dir, "strawberry.png")
thresh = 100

img = cv2.imread(PATH)


img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_flip = cv2.flip(img_gray, 0)
_, img_bin = cv2.threshold(img_flip, thresh, 255, cv2.THRESH_BINARY)
#res = cv2.resize(img_bin, (img_bin.shape[1]//2, img_bin.shape[0]//2))

res = img_thin

cv2.imshow("gray", img_gray)
cv2.imshow("bin", res)

bmp = potrace.Bitmap(res)
path = bmp.trace()

# --- Convert path to SVG string with line breaks ---
def path_to_svg(path, width, height):
    svg_path_lines = []
    for curve in path:
        start = curve.start_point
        svg_path_lines.append(f"M {start.x} {start.y}")
        for segment in curve:
            if segment.is_corner:
                c = segment.c
                svg_path_lines.append(f"L {c.x} {c.y}")
                svg_path_lines.append(f"L {segment.end_point.x} {segment.end_point.y}")
            else:
                c1, c2 = segment.c1, segment.c2
                svg_path_lines.append(
                    f"C {c1.x} {c1.y}, {c2.x} {c2.y}, {segment.end_point.x} {segment.end_point.y}"
                )
        svg_path_lines.append("Z\n")  # close path and new line

    svg_path = "\n".join(svg_path_lines)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
  <g transform="scale(1,-1) translate(0, -{height})">
    <path d="
{svg_path}
" fill="none" stroke="black" stroke-width="0.5" />
  </g>
</svg>"""
    return svg

svg_string = path_to_svg(path, res.shape[1], res.shape[0])

# Save to file
with open("trace.svg", "w") as f:
    f.write(svg_string)

cv2.waitKey(0)
