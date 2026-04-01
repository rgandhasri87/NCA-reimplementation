TARGET_PADDING = 16         # pad target image border
TARGET_SIZE = 40            # 40px by 40px base image

import io
import PIL.Image
import requests

import numpy as np

import torch
import torch.nn.functional as F


def load_image(url, max_size=TARGET_SIZE):
  r = requests.get(url)
  img = PIL.Image.open(io.BytesIO(r.content))
  img.thumbnail((max_size, max_size), PIL.Image.LANCZOS)
  img = np.float32(img) / 255.0

  # premultiply RGB values by Alpha value
  # img is 4 channel RGBA image
  # multiply by img[..., 3:] for numpy broadcasting: alpha channel has shape (H, W, 1) and rgb has shape (H, W, 3)
  img[..., :3] *= img[..., 3:]

  return img
  

def load_emoji(emoji):
  code = hex(ord(emoji))[2:].lower()
  url = f"https://github.com/googlefonts/noto-emoji/blob/main/png/128/emoji_u{code}.png?raw=true"
  return load_image(url)


def to_rgba(img):
  return img[..., :4]


def to_alpha(img):
  return torch.clamp(img[..., 3:4], 0.0, 1.0)


def to_rgb(img):
  # convert RGBA image to RGB by blending with white background (the 1.0)
  # assume rgb premultiplied by alpha
  rgb, a = img[..., :3], to_alpha(img)
  return 1.0 - a + rgb


def get_living_mask(img_batch):
  # first dimension is batch, then height, width, channels (here, only alpha)
  alpha = img_batch[:, :, :, 3:4]

  # permute because pytorch maxpool2d expects (batch, channels, height dimension, width dimension)
  alpha = alpha.permute(0, 3, 1, 2)

  max_pool = F.max_pool2d(alpha, 3, stride=1, padding=1)    # need padding of 1 for 3x3 window

  max_pool.permute(0, 2, 3, 1)    # return to batch, height, width, channel dimensions

  # return cells with either it or any neighbor (from the maxpool) having alpha value > 0.1 - these are considered the alive cells
  return max_pool > 0.1