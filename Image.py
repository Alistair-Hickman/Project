from PIL import Image
import numpy as np
import pandas as pd

open_path = "/Users/alistair/Documents/Project/Scripts/Trajectories/trajectory_0.csv"
df = pd.read_csv(open_path, usecols = ["X", "Y", "Z"], sep = "\t")
x_col = df["X"]
y_col = df["Y"]

x_init = 512
y_init = 512

x_lower = x_init - 10
x_upper = x_init + 10

y_lower = y_init - 10
y_upper = y_init + 10
for i in range (5):
    w, h = 1024, 1024
    data = np.zeros((h, w, 3), dtype=np.uint8)
    data[x_lower:x_upper, y_lower:y_upper] = [0, 0, 255] # blue patch
    img = Image.fromarray(data, 'RGB')
    path = "/Users/alistair/Documents/Project/Scripts/Frames/Frame_" + str(i) + ".png"
    img.save(path)

    x_upper += 5
    x_lower += 5
    y_upper += 5
    y_lower += 5
