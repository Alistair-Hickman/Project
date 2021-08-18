import numpy as np
import pandas as pd
import math
from PIL import Image
from multiprocessing import Pool

x_col = {}
y_col = {}
z_col = {}

x_vals = []
y_vals = []
z_vals = []

x_pos = []
y_pos = []
z_con = []

no_frames = 240

no_bugs = 2

for ii in range (no_bugs):
  open_path = "/Users/alistair/Documents/Project/Scripts/Trajectories.nosync/trajectory_" + str(ii) + ".csv"
  df = pd.read_csv(open_path, usecols = ["X", "Y", "Z"], sep = "\t")
  x_bug = df["X"]
  y_bug = df["Y"]
  z_bug = df["Z"]
  x_col["X%s" %ii] = x_bug
  x_vals.append(x_col["X%s" %ii] )

  y_col["Y%s" %ii] = y_bug
  y_vals.append(y_col["Y%s" %ii])

  #z_col["Z%s" %ii] = z_bug
  #z_vals.append(z_col["Z%s" %ii])


coords = []
#Periodic boundaries with 20% buffer
upper_boundary = int(1024*1.2)
lower_boundary = int(0-(upper_boundary - 1024))

q = 128
p = -1*np.sqrt(q)

sigma = 2.5
#Set up image array and reserve memory using np.zeros()
x, y = 1024, 1024
data = np.zeros((x, y, 3), dtype=np.uint8)
width = 5.0 #width in microns
ppm = float(x)/width #Calculate pixels per micron


for i in range(no_frames):
    for ii in range(no_bugs):
     #Calculate x and y positions by converting array position to pixel values
     x_pos.append(int((x_vals[ii][i]*ppm)+512))
     y_pos.append(int((y_vals[ii][i]*ppm)+512))
     #z_con.append(int(np.sqrt(z_vals[ii][i]*z_vals[ii][i]+2.0*z_vals[ii][i]*p+p*p)+q))

    #Periodic boudnary conditions - 20% buffer either side, will reenter opposite side of array.
    #Check logic - code seems good
    for l in range (len(x_pos)):
     if((abs(x_pos[l]) or abs(y_pos[l])) > upper_boundary or (abs(y_pos[l]) or abs(x_pos[l])) < lower_boundary):
        x_delta = x_pos[l] - 512
        y_delta = y_pos[l] - 512
        x_pos[l] = 512 - x_delta
        y_pos[l] = 512 - y_delta

    #Create array list of coordinates in pixels of bacteria - optional
    #coordinates = np.array([i, x_pos, y_pos], dtype=object)
    #coords.append(x_pos)

    for j in range(x):
        for k in range(y):
            val = 0
            for kk in range (len(x_pos)):
              val = 255*math.exp(-((j-x_pos[kk])*(j-x_pos[kk]))/(2.0 * sigma * sigma)) * math.exp(-((k-y_pos[kk])*(k-y_pos[kk]))/(2.0 * sigma * sigma))
            data[j,k] = [val,val,val]
            #print("test_3")

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
    z_con.clear()

#np.savetxt("/Users/alistair/Documents/Project/Scripts/Frames.nosync/coordinates.txt", coords)
