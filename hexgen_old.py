from PIL import Image
import sys
import tkinter as tk
from tkinter import filedialog

def rgb_to_rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

def rgb_to_4bit_gray(r, g, b):
    gray = int(0.299 * r + 0.587 * g + 0.114 * b)
    return gray >> 4  # 0–15

def rgb_to_8bit_gray(r, g, b):
    return int(0.299 * r + 0.587 * g + 0.114 * b)

def rgb_to_1bit_bw(r, g, b, threshold=128):
    gray = int(0.299 * r + 0.587 * g + 0.114 * b)
    return 1 if gray > threshold else 0

def pick_image_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    return file_path

def main():
    print("📂 Select an image file to convert...")
    img_path = pick_image_file()
    if not img_path:
        print("No file selected. Exiting.")
        sys.exit()

    try:
        img = Image.open(img_path).convert("RGB")
    except:
        print("Error: Cannot open image.")
        sys.exit()

    width = int(input("Enter target width: "))
    height = int(input("Enter target height: "))
    img = img.resize((width, height), Image.LANCZOS)

    print("\nSelect output format:")
    print("0. 1-bit monochrome (packed, 8 pixels per byte)")
    print("1. 4-bit grayscale (packed, 2 pixels per byte)")
    print("2. 8-bit grayscale")
    print("3. RGB565 color")
    choice = input("Enter choice (0-3): ").strip()

    hex_array = []

    if choice == "0":
        for y in range(height):
            for x in range(0, width, 8):
                byte_val = 0
                for bit in range(8):
                    if x + bit < width:
                        r, g, b = img.getpixel((x + bit, y))
                        bit_val = rgb_to_1bit_bw(r, g, b)
                        byte_val |= (bit_val << (7 - bit))
                hex_array.append(f"0x{byte_val:02X}")
        array_size = f"({width}*{height})/8"

    elif choice == "1":
        for y in range(height):
            for x in range(0, width, 2):
                r1, g1, b1 = img.getpixel((x, y))
                r2, g2, b2 = img.getpixel((x + 1, y)) if x + 1 < width else (0, 0, 0)
                gray1 = rgb_to_4bit_gray(r1, g1, b1)
                gray2 = rgb_to_4bit_gray(r2, g2, b2)
                packed_byte = (gray1 << 4) | gray2
                hex_array.append(f"0x{packed_byte:02X}")
        array_size = f"({width}*{height})/2"

    elif choice == "2":
        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                val = rgb_to_8bit_gray(r, g, b)
                hex_array.append(f"0x{val:02X}")
        array_size = f"{width}*{height}"

    elif choice == "3":
        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                val = rgb_to_rgb565(r, g, b)
                hex_array.append(f"0x{val:04X}")
        array_size = f"{width}*{height}"

    else:
        print("Invalid choice.")
        return

    var_name = input("Enter variable name (e.g., pic1): ").strip()
    file_name = input("Enter output filename (without extension): ").strip()
    if not file_name.lower().endswith(".txt"):
        file_name += ".txt"

    output_lines = []
    output_lines.append(f"const uint32_t {var_name}_width = {width};")
    output_lines.append(f"const uint32_t {var_name}_height = {height};")
    output_lines.append(f"const uint8_t {var_name}_data[{array_size}] = {{")

    for i in range(0, len(hex_array), 16):
        output_lines.append("    " + ", ".join(hex_array[i:i+16]) + ",")

    output_lines.append("};\n")

    with open(file_name, "w") as f:
        f.write("\n".join(output_lines))

    print(f"✅ Data saved to {file_name} in format choice {choice}")

if __name__ == "__main__":
    main()
