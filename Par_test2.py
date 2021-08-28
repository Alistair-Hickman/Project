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

no_bugs = 150

#Periodic boundaries with 20% buffer
upper_boundary = int(1024)
lower_boundary = int(0)

def main_loop(no_bugs):
 q = 128.0
 p = -0.01
 sigma = 2.5
 no_frames = 480
#Set up image array and reserve memory using np.zeros()
 x, y = 1024, 1024
 data = np.zeros((x, y, 3), dtype=np.uint8)
 width = 5.0 #width of image in microns
 ppm = float(x)/width #Calculate pixels per micron


 for i in range(140, 480):
    for ii in range(no_bugs):
     #Calculate x and y positions by converting array position to pixel values
     x_pos.append(int((x_vals[ii][i]*ppm)+512))
     y_pos.append(int((y_vals[ii][i]*ppm)+512))
     z_con.append((p*z_vals[ii][i]*z_vals[ii][i])+q)

    #Periodic boudnary conditions - 20% buffer either side, will reenter opposite side of array.
    #Check logic - code seems good
    for l in range (len(x_pos)):
     if((abs(x_pos[l]) or abs(y_pos[l])) >= 1024 or (abs(y_pos[l]) or abs(x_pos[l])) <= 0):
        x_delta = x_pos[l] - 512
        y_delta = y_pos[l] - 512
        x_pos[l] = 512 - x_delta
        y_pos[l] = 512 - y_delta


    for ll in range (len(x_pos)):

     x_max = x_pos[ll] + 10
     x_min = x_pos[ll] - 10
     y_max = y_pos[ll] + 10
     y_min = y_pos[ll] - 10
     for j in range(x_min, x_max):
        for k in range(y_min, y_max):
          val = 0
          for kk in range(len(x_pos)):
             val += z_con[kk]*math.exp(-((j-x_pos[kk])*(j-x_pos[kk]))/(2.0 * sigma * sigma)) * math.exp(-((k-y_pos[kk])*(k-y_pos[kk]))/(2.0 * sigma * sigma))
             if val > 255.0:
              val = 255.0
             elif val < 0:
              val = 0.0
          if (j < 1024 and j > 0 and k < 1024 and k > 0):
           data[j,k] = [val,val,val]


    #Image creation code
    for xx in range(1024):
        for yy in range(1024):
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
  x_col["X%s" %ii] = x_bug
  x_vals.append(x_col["X%s" %ii] )

  y_col["Y%s" %ii] = y_bug
  y_vals.append(y_col["Y%s" %ii])

  z_col["Z%s" %ii] = z_bug
  z_vals.append(z_col["Z%s" %ii])

if __name__ == '__main__':
  proc = mp.Process(target = main_loop(no_bugs))
  proc.start()