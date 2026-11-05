"""Draw the two finite graph examples; no empirical or convergence claim."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def generate() -> None:
    target = Path(__file__).resolve().parents[1] / "public_export"
    target.mkdir(exist_ok=True)
    image = Image.new("RGB", (1400, 560), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=28)
    title_font = ImageFont.load_default(size=34)
    draw.text((45, 25), "Declared graph extensions and homology", font=title_font, fill="black")
    draw.text((45, 90), "Two isolated vertices", font=font, fill="black")
    draw.text((750, 90), "Triangle with an attached face", font=font, fill="black")
    for x, label in ((100, "a"), (460, "b")):
        draw.ellipse((x-15, 225, x+15, 255), fill="#315d8a")
        draw.text((x-8, 270), label, font=font, fill="black")
    draw.line((120, 240, 440, 240), fill="#bf602a", width=5)
    draw.polygon(((440, 240), (423, 230), (423, 250)), fill="#bf602a")
    draw.text((150, 190), "added edge e", font=font, fill="#bf602a")
    vertices = ((810, 315), (1260, 315), (1035, 155))
    draw.polygon(vertices, fill="#e4edf4", outline="#315d8a", width=5)
    for (x, y), label in zip(vertices, "abc", strict=True):
        draw.ellipse((x-12, y-12, x+12, y+12), fill="#315d8a")
        draw.text((x-8, y+18), label, font=font, fill="black")
    draw.text((985, 245), "face f", font=font, fill="black")
    draw.text((45, 380), "H0 rank: 2 to 1; boundary(e) = b - a", font=font, fill="black")
    draw.text((750, 380), "H1 rank: 1 to 0; boundary(f) = cycle", font=font, fill="black")
    draw.text((45, 465), "Exact finite examples. Killing the old class prevents a chain-map retraction fixing it.",
              font=font, fill="black")
    image.save(target / "graph_extensions.png")
    print("Generated graph_extensions.png: the manuscript's declared finite examples")


if __name__ == "__main__":
    generate()
