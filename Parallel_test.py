import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from PIL import Image
from multiprocessing import Pool

x_col = []
y_col = []
z_col = []

x_pos = []
y_pos = []
z_con = []

no_frames = 10

no_bugs = 2

for ii in range (no_bugs):
  open_path = "/Users/alistair/Documents/Project/Scripts/Trajectories.nosync/trajectory_" + str(ii) + ".csv"
  df = pd.read_csv(open_path, usecols = ["X", "Y", "Z"], sep = "\t")
  x_bug = df["X"]
  y_bug = df["Y"]
  z_bug = df["Z"]
  x_col.append(x_bug)
  y_col.append(y_bug)
  z_col.append(z_bug)
  print("test_1")

coords = []
#Periodic boundaries with 20% buffer
upper_boundary = int(1024*1.2)
lower_boundary = int(0-(upper_boundary - 1024))

#q = 128
#p = -0.5*np.sqrt(q)

sigma = 5.0
#Set up image array and reserve memory using np.zeros()
x, y = 1024, 1024
data = np.zeros((x, y, 3), dtype=np.uint8)
width = 5.0 #width in microns
ppm = float(x)/width #Calculate pixels per micron


for i in range(no_frames):
    for jj in range(i, (i+no_bugs_1)):
     #Calculate x and y positions by converting array position to pixel values
     x_pos.append(int((x_col[jj][i]*ppm)+512))
     y_pos.append(int((y_col[jj][i]*ppm)+512))
     print("Test_2")
     #z_con.append((z_col[jj][i]-p)*(z_col[jj][i]-p)-q)

    #Periodic boudnary conditions - 20% buffer either side, will reenter opposite side of array.
    #Check logic - code seems good
    #if((abs(x_pos) or abs(y_pos)) > upper_boundary or (abs(y_pos) or abs(x_pos)) < lower_boundary):
        #x_delta = x_pos - 512
        #y_delta = y_pos - 512
        #x_pos = 512 - x_delta
        #y_pos = 512 - y_delta

    #Create array list of coordinates in pixels of bacteria - optional
    #coordinates = np.array([i, x_pos, y_pos])
    #coords.append(coordinates)

    for j in range(x):
        val = 0
        for k in range(y):
            for kk in range (no_bugs):
              val += 50*math.exp(-((j-x_pos[kk])*(j-x_pos[kk]))/(2.0 * sigma * sigma)) * math.exp(-((k-y_pos[kk])*(k-y_pos[kk]))/(2.0 * sigma * sigma))
              data[j,k] = [val,val,val]
              print("test_3")

    #Values are inserted into array for bliue square, will change with functions
    #to iterate over array and assign colour values normally
    #data[x_lower:x_upper, y_lower:y_upper] = [0, 0, 255] # blue patch
    #Image creation code
    im= Image.fromarray(data)
    im.save("/Users/alistair/Documents/Project/Scripts/Frames.nosync/Frame_" + str(i) + ".png")
    #Reset array to zero after each image to avoid artefacts from previous iteration.
    data = np.zeros((x, y, 3), dtype=np.uint8)
    x_pos.clear()
    y_pos.clear()
    z_pos.clear()
    z_con.clear()

#np.savetxt("/Users/alistair/Documents/Project/Scripts/Frames.nosync/coordinates.txt", coords)
