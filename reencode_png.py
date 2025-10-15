from PIL import Image
import os

# Path to your PNG
image_path = os.path.join("data", "icons", "covid-19.png")

# Open the image with Pillow
img = Image.open(image_path)

# Force-convert to standard RGBA and resave as a proper PNG
img = img.convert("RGBA")
fixed_path = os.path.join("data", "icons", "covid-19_fixed.png")
img.save(fixed_path, format="PNG")

print(f"✅ Fixed PNG saved at: {fixed_path}")
