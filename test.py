from pyxelate import Pyxelate
from skimage import io
import matplotlib.pyplot as plt
import cv2

img = io.imread("dataset/Tien.jpg")
# generate pixel art that is 1/14 the size
height, width, _ = img.shape 
factor = 2
colors = 32
dither = False

p = Pyxelate(height // factor, width // factor, colors, dither)
img_small = p.convert(img)  # convert an image with these settings

_, axes = plt.subplots(1, 2, figsize=(16, 16))
axes[0].imshow(img)
axes[1].imshow(img_small)
plt.show()