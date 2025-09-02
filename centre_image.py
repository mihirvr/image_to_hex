from PIL import Image
import tkinter as tk
from tkinter import filedialog
import os

# Preset border colors
BORDER_COLORS = {
    "1": ("Black", (0, 0, 0)),
    "2": ("Dark Gray", (85, 85, 85)),
    "3": ("Medium Gray", (170, 170, 170)),
    "4": ("Light Gray", (220, 220, 220)),
    "5": ("White", (255, 255, 255))
}

def pick_image_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )

def main():
    print("📂 Select the image you want to process...")
    img_path = pick_image_file()
    if not img_path:
        print("❌ No file selected. Exiting.")
        return

    try:
        img = Image.open(img_path).convert("RGB")
    except Exception as e:
        print(f"❌ Error opening image: {e}")
        return

    # Ask for target dimensions
    target_width = int(input("Enter target width (e.g., 960): "))
    target_height = int(input("Enter target height (e.g., 540): "))

    # Ask user for border color
    print("\nChoose border color:")
    for k, (name, rgb) in BORDER_COLORS.items():
        print(f"{k}. {name}")
    choice = input("Enter choice (1-5): ").strip()
    if choice not in BORDER_COLORS:
        print("❌ Invalid choice. Defaulting to black.")
        choice = "1"
    border_rgb = BORDER_COLORS[choice][1]

    # Create new background with chosen color
    background = Image.new("RGB", (target_width, target_height), border_rgb)

    # Scale down if image is bigger than target
    img.thumbnail((target_width, target_height), Image.LANCZOS)

    # Calculate position to center image
    paste_x = (target_width - img.width) // 2
    paste_y = (target_height - img.height) // 2

    # Paste the image onto the background
    background.paste(img, (paste_x, paste_y))

    # Prepare output folder
    output_dir = os.path.join(os.getcwd(), "centred")
    os.makedirs(output_dir, exist_ok=True)

    # Save result into centred folder
    output_file = input("Enter output filename (without extension): ").strip() + ".png"
    save_path = os.path.join(output_dir, output_file)
    background.save(save_path)
    print(f"✅ Saved centered image with borders as {save_path}")

if __name__ == "__main__":
    main()
