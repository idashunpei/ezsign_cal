import argparse
from io import BytesIO
from pathlib import Path

import pymupdf
from PIL import Image
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

WIDTH = 400
HEIGHT = 300
SOURCE = Path(__file__).with_name("cal.png")
OUTPUT = Path(__file__).with_name("cal_epaper.png")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PALETTE = (BLACK, WHITE, RED, YELLOW)


def nearest_palette(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    r, g, b = rgb[:3]

    # Treat gray edge pixels by distance to the four output colors. This
    # keeps the nearest-result image crisp without generating intermediates.
    return min(
        PALETTE,
        key=lambda color: (
            (r - color[0]) ** 2
            + (g - color[1]) ** 2
            + (b - color[2]) ** 2
        ),
    )


def load_source(source: Path) -> Image.Image:
    if source.suffix.lower() == ".svg":
        drawing = svg2rlg(str(source))
        scale = min(WIDTH / drawing.width, HEIGHT / drawing.height)
        drawing.width *= scale
        drawing.height *= scale
        drawing.scale(scale, scale)
        pdf_data = renderPDF.drawToString(drawing)
        with pymupdf.open(stream=pdf_data, filetype="pdf") as document:
            page = document.load_page(0)
            pixmap = page.get_pixmap(dpi=96, alpha=False)
            rendered = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
        return rendered.resize((WIDTH, HEIGHT), Image.Resampling.NEAREST)

    with Image.open(source) as image:
        return image.convert("RGB").resize(
            (WIDTH, HEIGHT), Image.Resampling.NEAREST
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert an SVG or PNG to a 400x300, four-color e-paper image."
    )
    parser.add_argument("source", nargs="?", type=Path, default=SOURCE)
    parser.add_argument("output", nargs="?", type=Path)
    args = parser.parse_args()

    output = args.output or args.source.with_name(
        f"{args.source.stem}_epaper.png"
    )
    with load_source(args.source) as source:
        pixels = [nearest_palette(pixel) for pixel in source.getdata()]
        result = Image.new("RGB", (WIDTH, HEIGHT))
        result.putdata(pixels)
        result.save(output, format="PNG", optimize=True)

    print(f"Created {output}")


if __name__ == "__main__":
    main()
