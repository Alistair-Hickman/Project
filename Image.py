import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from PIL import Image

open_path = "/Users/alistair/Documents/Project/Scripts/Trajectories.nosync/trajectory_1.csv"
df = pd.read_csv(open_path, usecols = ["X", "Y", "Z"], sep = "\t")
x_col = df["X"]
y_col = df["Y"]
z_col = df["Z"]

coords = []
#Periodic boundaries with 20% buffer
upper_boundary = int(1024*1.2)
lower_boundary = int(0-(upper_boundary - 1024))

q = 128
p = -1*np.sqrt(q)

sigma = 5.0
#Set up image array and reserve memory using np.zeros()
x, y = 1024, 1024
data = np.zeros((x, y, 3), dtype=np.uint8)
width = 5.0 #width in microns
ppm = float(x)/width #Calculate pixels per micron


for i in range(500):
    #Calculate x and y positions by converting array position to pixel values
    x_pos = int((x_col[i]*ppm)+512)
    y_pos = int((y_col[i]*ppm)+512)
    z_con = int((z_col[i]-p)*(z_col[i]-p)-q)

    #Periodic boudnary conditions - 20% buffer either side, will reenter opposite side of array.
    #Check logic - code seems good
    if((abs(x_pos) or abs(y_pos)) > upper_boundary or (abs(y_pos) or abs(x_pos)) < lower_boundary):
        x_delta = x_pos - 512
        y_delta = y_pos - 512
        x_pos = 512 - x_delta
        y_pos = 512 - y_delta

    #Create array list of coordinates in pixels of bacteria - optional
    #coordinates = np.array([i, x_pos, y_pos])
    #coords.append(coordinates)

    for j in range(x):
        for k in range(y):
            val = z_con * math.exp(-((j-x_pos)*(j-x_pos))/(2.0 * sigma * sigma)) * math.exp(-((k-y_pos)*(k-y_pos))/(2.0 * sigma * sigma))
            data[j,k] = [val,val,val]

    #Values are inserted into array for bliue square, will change with functions
    #to iterate over array and assign colour values normally
    #data[x_lower:x_upper, y_lower:y_upper] = [0, 0, 255] # blue patch
    #Image creation code
    im= Image.fromarray(data)
    im.save("/Users/alistair/Documents/Project/Scripts/Frames.nosync/Frame_" + str(i) + ".png")
    #Reset array to zero after each image to avoid artefacts from previous iteration.
    data = np.zeros((x, y, 3), dtype=np.uint8)

#np.savetxt("/Users/alistair/Documents/Project/Scripts/Frames.nosync/coordinates.txt", coords)
