import os
from glob import glob
from PIL import Image
from customtkinter import CTkImage

class CardManager:
  def __init__(self):
    self.card_images = {}
    self.special_images = {}
    self.import_images()

  def import_images(self):
    SPECIAL = {'back', 'black', 'red', 'empty'}

    for path in glob('cards_cropped_resized/card_*.png'):
      filename = os.path.basename(path)
      name = filename.replace('.png', '').replace('card_', '')
      parts = name.split('_')

      with Image.open(path) as img:
        ctk_img = CTkImage(light_image=img.copy(), size=(84, 120))

      if parts[-1] in SPECIAL:
        self.special_images['_'.join(parts)] = ctk_img
      else:
        suit = parts[0]
        rank = self.normalize_rank(parts[-1])
        self.card_images[(rank, suit)] = ctk_img

  def normalize_rank(self, rank):
    if rank.isdigit():
      return str(int(rank))
    return rank.upper()