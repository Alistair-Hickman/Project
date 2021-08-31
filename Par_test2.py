import numpy as np
import pandas as pd
import math
from PIL import Image
import multiprocessing as mp

x_col = {}
y_col = {}
z_col = {}

x_vals = []
y_vals = []
z_vals = []

x_pos = []
y_pos = []
z_con = []

no_bugs = 200

#Periodic boundaries with 20% buffer
upper_boundary = int(1024*1.2)
lower_boundary = int(0-(upper_boundary-1024.0))

def main_loop(no_bugs):
 q = 128.0
 p = -0.0005
 sigma = 2.0
 no_frames = 2000
#Set up image array and reserve memory using np.zeros()
 x, y = 1024, 1024
 data = np.zeros((x, y, 3), dtype=np.uint8)
 width = 500 #width of image in microns
 ppm = float(x)/width #Calculate pixels per micron


 for i in range(1, no_frames, 5):
    for ii in range(no_bugs):
     #Calculate x and y positions by converting array position to pixel values
     x_pos.append(int((x_vals[ii][i]*ppm)+512))
     y_pos.append(int((y_vals[ii][i]*ppm)+512))
     z_con.append((p*z_vals[ii][i]*z_vals[ii][i])+q)

    #Periodic boudnary conditions - 20% buffer either side, will reenter opposite side of array.
    #Check logic - code seems good
    for l in range (len(x_pos)):
     if((x_pos[l] or y_pos[l]) >= upper_boundary or (y_pos[l] or x_pos[l]) <= lower_boundary):
        if (x_pos[l] == 0):
             x_delta = 0.833
             y_delta = upper_boundary%y_pos[l]
             x_pos[l] = int(abs(x_delta)*upper_boundary)
             y_pos[l] = int(abs(y_delta)*upper_boundary)
        elif (y_pos[l] == 0):
             x_delta = upper_boundary%x_pos[l]
             y_delta = 0.833
             x_pos[l] = int(abs(x_delta)*upper_boundary)
             y_pos[l] = int(abs(y_delta)*upper_boundary)
        else :
             x_delta = upper_boundary%x_pos[l]
             y_delta = upper_boundary%y_pos[l]
             x_pos[l] = int(abs(x_delta)*upper_boundary)
             y_pos[l] = int(abs(y_delta)*upper_boundary)




    for ll in range (len(x_pos)):
     x_max = x_pos[ll] + 8
     x_min = x_pos[ll] - 8
     y_max = y_pos[ll] + 8
     y_min = y_pos[ll] - 8
     for j in range(x_min, x_max):
        for k in range(y_min, y_max):
         if (j < 1024 and j > 0 and k < 1024 and k > 0):
          val = data[j,k]
          val += np.uint8(z_con[ll]*math.exp(-((j-x_pos[ll])*(j-x_pos[ll]))/(2.0 * sigma * sigma)) * math.exp(-((k-y_pos[ll])*(k-y_pos[ll]))/(2.0 * sigma * sigma)))

          #data[j,k] = val


    #Image inversion code
    for xx in range(1024):
        for yy in range(1024):
          if np.any(data[xx,yy]) > 255.0:
            data[xx,yy] = 255.0
          elif np.any(data[xx,yy]) < 0:
            data[xx,yy] = 0
          data[xx,yy] = (data[xx,yy]*-1) + 255

    im= Image.fromarray(data)
    im.save("/Users/alistair/Documents/Project/Scripts/Frames2.nosync/Frame_" + str(i) + ".png")
    #Reset array to zero after each image to avoid artefacts from previous iteration.
    data = np.zeros((x, y, 3), dtype=np.uint8)
    x_pos.clear()
    y_pos.clear()
    z_con.clear()

 return 0


for ii in range (no_bugs):
  open_path = "/Users/alistair/Documents/Project/Scripts/Trajectories2.nosync/trajectory_" + str(ii) + ".csv"
  df = pd.read_csv(open_path, usecols = ["X", "Y", "Z"], sep = "\t")
  x_bug = df["X"]
  y_bug = df["Y"]
  z_bug = df["Z"]
  x_col["X%s"] = x_bug
  x_vals.append(x_col["X%s"] )

  y_col["Y%s"] = y_bug
  y_vals.append(y_col["Y%s"])

  z_col["Z%s"] = z_bug
  z_vals.append(z_col["Z%s"])

if __name__ == '__main__':
  proc = mp.Process(target = main_loop(no_bugs))
  proc.start()
