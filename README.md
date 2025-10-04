<meta name="google-site-verification" content="0tBfaHkhkYpJxBVEgsku7RFdMl9nqP8mjtDl5C-oBRM" />

# image_to_hex

This project provides a set of Python tools to convert images into hexadecimal arrays for use with microcontrollers (e.g., ESP32/Arduino) — especially for E-Ink displays.

✨ Features

•Image → Hex Conversion
✅ 1-bit monochrome
✅ Grayscale (4-bit / multi-shade)
✅ 1-bit monochrome with dithering (to mimic grayscale)

•Hex → Image Conversion
Verify hex array validity by converting back into an image.

•Image → Bitmap (.bmp)
Convert images into standard .bmp format for further processing.

•Centering Tool
Center a .png or image on a canvas.
Fills borders with 5 shades (black, white, and 3 gray levels).

🚀 Usage

•Clone the repo:

git clone https://github.com/mihirvr/image_to_hex.git

•Install dependencies:

pip install -r requirements.txt

•Run a script:

python hexgen_w_dithering.py

•Check outputs in respective folders


📌 Notes

Designed for E-Ink display testing (works with ESP32/Arduino projects).
Supports monochrome + grayscale (with and without dithering).

Easy preview to ensure the generated hex data is valid.

