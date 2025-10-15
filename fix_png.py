from PIL import Image
import os

# List all PNG files in the icons folder
icons_folder = os.path.join("data", "icons")

for file_name in os.listdir(icons_folder):
    if file_name.lower().endswith(".png"):
        file_path = os.path.join(icons_folder, file_name)
        try:
            img = Image.open(file_path)
            img = img.convert("RGBA")  # Convert to proper PNG format
            img.save(file_path)        # Overwrite original
            print(f"✅ Converted: {file_name}")
        except Exception as e:
            print(f"❌ Failed: {file_name} -> {e}")
