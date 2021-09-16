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
z_pos = []
z_cons = []

no_bugs = 200
x = 512
y = x
x_flt = 512.0
#Periodic boundaries with 20% buffer
upper_boundary = x_flt*1.2
lower_boundary = 0-(upper_boundary-x_flt)

def main_loop(no_bugs,x,y):
 #Variables for z quadratic - I = p*z^2 + q
 q = 100
 p = -0.00284
 sigma = 1.0

 no_frames = 400000
 frame_spacing = 50
#Set up image array and reserve memory using np.zeros()

 data = np.zeros((x, y, 3), dtype=np.uint8)
 width = 750 #width of image in microns
 ppm = float(x)/width #Calculate pixels per micron


 for i in range(0,no_frames,frame_spacing):
    for ii in range(no_bugs):
     #Calculate x and y positions by converting array position to pixel values
     x_pos.append(int(x_vals[ii][i]*ppm))
     y_pos.append(int(y_vals[ii][i]*ppm))
     z_pos.append(int(z_vals[ii][i]*ppm))


    #Periodic boudnary conditions - 20% buffer either side, will reenter opposite side of array.
    #Check logic - code seems good
    for g in range (len(x_pos)):
     if(x_pos[g] > upper_boundary or x_pos[g] < lower_boundary):
         x_pos[g] = int(x_pos[g] % upper_boundary)
     if(y_pos[g] > upper_boundary or y_pos[g] < lower_boundary):
         y_pos[g] = int(y_pos[g] % upper_boundary or y_pos[g] < lower_boundary)
     if(z_pos[g] > upper_boundary or z_pos[g] < lower_boundary):
         z_pos[g] = int(z_pos[g] % upper_boundary)

    #np.savetxt("/Users/alistair/Documents/Project/Scripts/Trajectories2.nosync/z_pos.csv", z_pos)
    for zz in range(len(z_pos)):
     z_temp = (z_pos[zz])/ppm
     z_con = 0
     z_con += p*abs(z_temp)*abs(z_temp)
     if abs(z_con) > q :
         z_con = 0
     else:
         z_con = z_con + q
     z_cons.append(z_con)

    #np.savetxt("/Users/alistair/Documents/Project/Scripts/Trajectories2.nosync/z_vals.csv", z_cons)
    for ll in range (len(x_pos)):
     x_max = x_pos[ll] + 8
     x_min = x_pos[ll] - 8
     y_max = y_pos[ll] + 8
     y_min = y_pos[ll] - 8
     for j in range(x_min, x_max):
        for k in range(y_min, y_max):
         if (j < x and j > 0 and k < x and k > 0):
          val = data[j,k]
          val += np.uint8(z_cons[ll]*math.exp(-((j-x_pos[ll])*(j-x_pos[ll]))/(2.0 * sigma * sigma)) * math.exp(-((k-y_pos[ll])*(k-y_pos[ll]))/(2.0 * sigma * sigma)))
          data[j,k] = val


    #Image inversion code
    for xx in range(x):
        for yy in range(y):
          data[xx,yy] = (data[xx,yy] * -1) + 255


    im= Image.fromarray(data)
    im.save("/Users/alistair/Documents/Project/Scripts/50_Frames1.nosync/Frame_" + str(i) + ".png")
    #Reset array to zero after each image to avoid artefacts from previous iteration.
    data = np.zeros((x, y, 3), dtype=np.uint8)
    x_pos.clear()
    y_pos.clear()
    z_pos.clear()
    z_cons.clear()

 return 0


for ii in range (no_bugs):
  open_path = "/Users/alistair/Documents/Project/Scripts/50_trajectories1.nosync/trajectory_" + str(ii) + ".csv"
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
  proc = mp.Process(target = main_loop(no_bugs,x,y))
  proc.start()
