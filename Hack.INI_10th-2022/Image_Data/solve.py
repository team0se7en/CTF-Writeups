from PIL import Image
import numpy as np

import json

data = None

with open('imageData.json') as json_file:
    data = json.load(json_file)["data"]

px = []
for i in range(len(data)//4):
    px.append((data[str(i*4)], data[str(i*4+1)], data[str(i*4+2)], data[str(i*4+3)]))

pixels = []

for i in range(80):
    x = []
    x.extend(px[i*500:(i+1)*500])
    pixels.append(x)

# Convert the pixels into an array using numpy
array = np.array(pixels, dtype=np.uint8)

# Use PIL to create an image from the new array of pixels
new_image = Image.fromarray(array, "RGBA")
new_image.save('flag.png')