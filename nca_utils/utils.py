TARGET_PADDING = 16         # pad target image border
TARGET_SIZE = 40            # 40px by 40px base image

import io
import PIL
import requests

import numpy as np


def load_image(url, max_size=TARGET_SIZE):
  r = requests.get(url)
  img = PIL.Image.open(io.BytesIO(r.content))
  img.thumbnail((max_size, max_size), PIL.Image.LANCZOS)
  img = np.float32(img) / 255.0

  # premultiply RGB values by Alpha value
  # img is 4 channel RGBA image
  # multiply by img[..., 3:] for numpy broadcasting
  img[..., :3] *= img[..., 3:]

  return img
  

def load_emoji(emoji):
  code = hex(ord(emoji))[2:].lower()
  url = f"https://github.com/googlefonts/noto-emoji/blob/main/png/128/emoji_u{code}.png?raw=true"
  return load_image(url)