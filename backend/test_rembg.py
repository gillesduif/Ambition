from rembg import remove
from PIL import Image
import io

# Pad naar je afbeelding
input_path = "/Users/gillesdhuyvetter/Pictures/girl-3.jpg"
output_path = "/Users/gillesdhuyvetter/Pictures/processed_girl-3.png"

try:
    # Open het bestand en lees de bytes
    with open(input_path, "rb") as f:
        img_data = f.read()
        print(f"Image data loaded successfully: {len(img_data)} bytes")

    # Achtergrond verwijderen met rembg
    print("Starting background removal...")
    output_data = remove(img_data)
    print("Background removal completed.")

    # Verwerkte afbeelding openen en opslaan
    with Image.open(io.BytesIO(output_data)) as img:
        img.save(output_path, "PNG")
        print(f"Processed image saved successfully to: {output_path}")

except Exception as e:
    print(f"Error: {e}")
