import glob
from PIL import Image
import os

output_folder = "cards_cropped_resized"
os.makedirs(output_folder, exist_ok=True)

for file in glob.glob("Cards (large)/*.png"):
  img = Image.open(file)
  cropped = img.crop((11,2,53,62))

  aspect_ratio = cropped.width / cropped.height

  new_height = 120
  new_width = aspect_ratio * new_height

  resized_image = cropped.resize((int(new_width), int(new_height)))

  filename = os.path.basename(file)
  new_path = os.path.join(output_folder, filename)

  resized_image.save(new_path)