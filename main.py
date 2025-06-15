import os
import argparse
from pathlib import Path
from PIL import Image

def extract_sprites(image_path, output_folder, bg_color=None, output_format="png"):
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size
    pixels = image.load()

    visited = [[False for _ in range(height)] for _ in range(width)]
    sprites = []

    def is_opaque(x, y):
        return image.getpixel((x, y))[3] > 0

    def flood_fill(x, y, bbox):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (0 <= cx < width and 0 <= cy < height and
                not visited[cx][cy] and is_opaque(cx, cy)):
                visited[cx][cy] = True
                bbox[0] = min(bbox[0], cx)
                bbox[1] = min(bbox[1], cy)
                bbox[2] = max(bbox[2], cx)
                bbox[3] = max(bbox[3], cy)
                stack.extend([
                    (cx + 1, cy), (cx - 1, cy),
                    (cx, cy + 1), (cx, cy - 1)
                ])

    for x in range(width):
        for y in range(height):
            if not visited[x][y] and is_opaque(x, y):
                bbox = [x, y, x, y]
                flood_fill(x, y, bbox)
                sprites.append(tuple(bbox))

    os.makedirs(output_folder, exist_ok=True)

    for i, (x1, y1, x2, y2) in enumerate(sprites):
        cropped = image.crop((x1, y1, x2 + 1, y2 + 1))
        output_path = output_folder / f"sprite_{i + 1}.{output_format.lower()}"

        if bg_color is not None:
            # Add solid background instead of transparency
            bg_image = Image.new("RGB", cropped.size, bg_color)
            bg_image.paste(cropped, mask=cropped.split()[3])  # Use alpha channel as mask
            bg_image.save(output_path, format=output_format.upper())
        else:
            cropped.save(output_path, format=output_format.upper())

        print(f"✅ Saved sprite {i+1} to: {output_path}")

    print(f"\n🎉 Done! Extracted {len(sprites)} sprites to '{output_folder}'.")

def parse_color(color_str):
    """Parses a hex or RGB color string into a tuple"""
    if "," in color_str:
        return tuple(map(int, color_str.split(",")))
    if color_str.startswith("#"):
        color_str = color_str[1:]
    if len(color_str) == 6:
        return tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4))
    raise ValueError("Invalid color format. Use '#RRGGBB' or 'R,G,B'")

def main():
    parser = argparse.ArgumentParser(description="Extract individual sprites from a PNG spritesheet with transparency.")
    parser.add_argument("image", help="Path to the spritesheet image")
    parser.add_argument("output", help="Output folder to save the individual sprites")
    parser.add_argument("--bg", help="Background color (e.g., '#ffffff' or '255,255,255') to replace transparency", default=None)
    parser.add_argument("--format", help="Output format: png (default) or jpg", choices=["png", "jpg"], default="png")

    args = parser.parse_args()

    image_path = Path(args.image).resolve()
    output_folder = Path(args.output).resolve()

    if not image_path.exists():
        print(f"❌ Error: Image file '{image_path}' does not exist.")
        return

    bg_color = parse_color(args.bg) if args.bg else None

    print(">>> Starting")
    print(">>> Image path: ", image_path)
    print(">>> Save path: ", output_folder)
    print(">>> BG: ", bg_color)
    print(">>> Format: ", args.format)

    extract_sprites(image_path, output_folder, bg_color=bg_color, output_format=args.format)

if __name__ == "__main__":
    main()
