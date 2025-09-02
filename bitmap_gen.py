import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def convert_to_1bit_bmp(input_path, output_path, size=(800, 480), dither=False):
    """
    Convert image to 1-bit monochrome BMP for eInk display
    - input_path: original image
    - output_path: saved BMP file
    - size: (width, height) tuple, e.g. (800, 480)
    - dither: True = Floyd-Steinberg dithering, False = pure threshold B/W
    """

    # Open and resize image
    img = Image.open(input_path).convert("RGB")
    img = img.resize(size, Image.Resampling.LANCZOS)  # FIXED

    # Convert to grayscale first
    img = img.convert("L")

    # Convert to 1-bit (mode "1" in PIL)
    if dither:
        img = img.convert("1", dither=Image.FLOYDSTEINBERG)
    else:
        img = img.convert("1", dither=Image.NONE)

    # Save as BMP (1-bit uncompressed)
    img.save(output_path, format="BMP")
    print(f"✅ Saved 1-bit BMP at {output_path}")

def main():
    # Open file picker
    root = tk.Tk()
    root.withdraw()  # hide GUI window

    print("Select input image...")
    input_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )

    if not input_path:
        print("No file selected, exiting.")
        return

    # Ask user for output resolution
    try:
        w = int(input("Enter width (default 800): ") or 800)
        h = int(input("Enter height (default 480): ") or 480)
    except ValueError:
        print("Invalid input, using default (800x480)")
        w, h = 800, 480

    # Ask user dithering preference
    dither_choice = input("Apply dithering? (y/n, default y): ").lower()
    dither = (dither_choice != "n")

    # Ask user for variable/file name
    file_var_name = input("Enter variable or file name (e.g. myImage): ").strip()
    if not file_var_name:
        file_var_name = "output"

    # Create Converted_Bitmap folder if not exists
    out_dir = os.path.join(os.getcwd(), "Converted_Bitmap")
    os.makedirs(out_dir, exist_ok=True)

    # Build full output path
    output_path = os.path.join(out_dir, f"{file_var_name}.bmp")

    # Run conversion
    convert_to_1bit_bmp(input_path, output_path, size=(w, h), dither=dither)

if __name__ == "__main__":
    main()
