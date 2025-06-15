# Spritesheet Slicer

Open-source script for auto slicing sprites from a spritsheet. It auto slices based on background: by default it considers background to be transparent, and isolates all sprites separated by the transparent background, and indivudally saves each one in a folder.

- Intall Python (tested with Python 3.12.11 on Mac M1 Sonoma)
- Install pillow (for image processing): ´pip install pillow´
- Run with default configs (image = spritesheet.png; save folder = "output" [both relative to script folder]; transparent bg; PNG save type):
´python main.py'
- To use custom Absolute/Relative paths, to pass other background color, or a different save format (jpg instead of png f.e.) pass args via CLI, f.e.:
´python main.py --image /Users/Me/documents/sprite-sheet-file.png --output output_dir --bg #ffffff --format jpg´
