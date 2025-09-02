from PIL import Image
import re
import tkinter as tk
from tkinter import filedialog
import sys

def pick_hex_file():
    """Open file picker dialog."""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Select HEX Data File",
        filetypes=[("Header/Text Files", "*.h;*.txt")]
    )

def main():
    print("📂 Select the HEX data file...")
    file_path = pick_hex_file()
    if not file_path:
        print("No file selected. Exiting.")
        sys.exit()

    with open(file_path, "r") as f:
        content = f.read()

    # Extract width & height from file
    match_w = re.search(r'width\s*=\s*(\d+)', content)
    match_h = re.search(r'height\s*=\s*(\d+)', content)
    if not match_w or not match_h:
        print("❌ Could not find width/height in file.")
        sys.exit()

    width = int(match_w.group(1))
    height = int(match_h.group(1))

    # Extract hex values
    hex_values = re.findall(r'0x[0-9A-Fa-f]+', content)
    if not hex_values:
        print("❌ No hex values found.")
        sys.exit()

    print("\nSelect data format used in the file:")
    print("1. 1-bit B/W")
    print("2. 4-bit grayscale")
    print("3. 8-bit grayscale")
    choice = input("Enter choice (1-3): ").strip()

    img = Image.new("L", (width, height))  # "L" = 8-bit grayscale in Pillow
    pixels = img.load()

    if choice == "1":
        # 1-bit unpack (8 pixels per byte)
        index = 0
        for y in range(height):
            for x in range(0, width, 8):
                byte_val = int(hex_values[index], 16)
                for bit in range(8):
                    if x + bit < width:
                        pixels[x + bit, y] = 0 if (byte_val & (0x80 >> bit)) else 255
                index += 1

    elif choice == "2":
        # 4-bit grayscale (two pixels per byte)
        index = 0
        for y in range(height):
            for x in range(0, width, 2):
                byte_val = int(hex_values[index], 16)
                high_nibble = (byte_val >> 4) & 0x0F
                low_nibble = byte_val & 0x0F
                pixels[x, y] = high_nibble * 17
                if x + 1 < width:
                    pixels[x + 1, y] = low_nibble * 17
                index += 1

    elif choice == "3":
        # 8-bit grayscale (one pixel per byte)
        index = 0
        for y in range(height):
            for x in range(width):
                pixels[x, y] = int(hex_values[index], 16)
                index += 1
    else:
        print("❌ Invalid choice.")
        sys.exit()

    img.show()
    print("✅ Preview opened in default image viewer.")

if __name__ == "__main__":
    main()
