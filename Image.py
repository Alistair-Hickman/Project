import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

open_path = "/Users/alistair/Documents/Project/Scripts/Trajectories.nosync/trajectory_0.csv"
df = pd.read_csv(open_path, usecols = ["X", "Y", "Z"], sep = "\t")
x_col = df["X"]
y_col = df["Y"]
z_col = df["Z"]

coords = []

#Gauss_func =

#Set up image array and reserve memory using np.zeros()
w, h = 1024, 1024
data = np.zeros((h, w, 3), dtype=np.uint8)
width = 5.0 #width in microns
ppm = float(w)/width
print(ppm)
#Calculate mid point for starting position
for i in range(50):
    x_pos = int((x_col[i]*ppm)+512)
    y_pos = int((y_col[i]*ppm)+512)

    coordinates = np.array([i, x_pos, y_pos])
    coords.append(coordinates)

    x_lower = x_pos - 10
    x_upper = x_pos + 10
    y_lower = x_pos - 10
    y_upper = x_pos + 10

    data[x_lower:x_upper, y_lower:y_upper] = [0, 0, 255] # blue patch
    im= Image.fromarray(data)
    im.save("/Users/alistair/Documents/Project/Scripts/Frames.nosync/Frame_" + str(i) + ".png")
    data = np.zeros((h, w, 3), dtype=np.uint8)

np.savetxt("/Users/alistair/Documents/Project/Scripts/Frames.nosync/coordinates.txt", coords)
