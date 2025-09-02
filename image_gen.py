from PIL import Image
import re
import sys
import os
import tkinter as tk
from tkinter import filedialog

def rgb565_to_rgb(val):
    r = (val >> 11) & 0x1F
    g = (val >> 5) & 0x3F
    b = val & 0x1F
    return (r << 3, g << 2, b << 3)

def gray4_to_rgb(val):
    g = val * 17
    return (g, g, g)

def gray8_to_rgb(val):
    return (val, val, val)

def bit_to_bw(bit_val):
    return (255, 255, 255) if bit_val else (0, 0, 0)

def pick_hex_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select HEX Data File",
        filetypes=[("Header/Text Files", "*.h;*.txt")]
    )
    return file_path

def main():
    print("📂 Select the HEX data file...")
    file_path = pick_hex_file()
    if not file_path:
        print("No file selected. Exiting.")
        sys.exit()

    with open(file_path, "r") as f:
        content = f.read()

    match_w = re.search(r'width\s*=\s*(\d+)', content)
    match_h = re.search(r'height\s*=\s*(\d+)', content)
    if not match_w or not match_h:
        print("Error: Could not find width/height in file.")
        sys.exit()

    width = int(match_w.group(1))
    height = int(match_h.group(1))

    hex_values = re.findall(r'0x[0-9A-Fa-f]+', content)
    if not hex_values:
        print("Error: No hex values found.")
        sys.exit()

    print("\nSelect data format used in the file:")
    print("0. 1-bit monochrome (packed, 8 pixels per byte)")
    print("1. 4-bit grayscale (packed, 2 pixels per byte)")
    print("2. 8-bit grayscale")
    print("3. RGB565 color")
    choice = input("Enter choice (0-3): ").strip()

    img = Image.new("RGB", (width, height))
    pixels = img.load()
    index = 0

    if choice == "0":
        for y in range(height):
            for x in range(0, width, 8):
                byte_val = int(hex_values[index], 16)
                for bit in range(8):
                    if x + bit < width:
                        pixels[x + bit, y] = bit_to_bw((byte_val >> (7 - bit)) & 1)
                index += 1

    elif choice == "1":
        for y in range(height):
            for x in range(0, width, 2):
                byte_val = int(hex_values[index], 16)
                gray1 = (byte_val >> 4) & 0x0F
                gray2 = byte_val & 0x0F
                pixels[x, y] = gray4_to_rgb(gray1)
                if x + 1 < width:
                    pixels[x + 1, y] = gray4_to_rgb(gray2)
                index += 1

    elif choice == "2":
        for y in range(height):
            for x in range(width):
                val = int(hex_values[index], 16)
                pixels[x, y] = gray8_to_rgb(val)
                index += 1

    elif choice == "3":
        for y in range(height):
            for x in range(width):
                val = int(hex_values[index], 16)
                pixels[x, y] = rgb565_to_rgb(val)
                index += 1
    else:
        print("Invalid choice.")
        sys.exit()

    # Create "generated" folder inside project directory
    output_dir = os.path.join(os.getcwd(), "Generated Image")
    os.makedirs(output_dir, exist_ok=True)

    # Use input filename as base name for output
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = os.path.join(output_dir, base_name + ".png")

    img.save(output_file)
    print(f"✅ Image saved as {output_file}")

if __name__ == "__main__":
    main()
