from PIL import Image
import numpy as np

#Radius in pixels
ppm = 0.711

x_low = 512 -
x_high = 512 +

y_low = 512 -
y_high = 512 +

#z_low
#z_high

w, h = 1024.0, 1024.0
data = np.zeros((h, w, 3), dtype=np.uint8)
data[particle_lower:particle_upper, particle_lower:particle_upper] = [0, 0, 255] # blue patch
img = Image.fromarray(data, 'RGB')
img.save('frame.png')
