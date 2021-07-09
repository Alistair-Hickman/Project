# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 13:32:35 2020o

@author: Alist
"""
import numpy as np
from numpy.random import seed
import random
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math
from numpy import savetxt
#from Matmul_fnc import tumble

def MSD(pos_arr):
  MSD_values = []
  displacements = []
  tau = []

  for j in range(20,1000):
    for i in range(1, len(pos_arr)):
         if (i-j) > 0:
          disp_x = pos_arr[i][0] - pos_arr[i-j][0]
          disp_y = pos_arr[i][1] - pos_arr[i-j][1]
          disp_z = pos_arr[i][2] - pos_arr[i-j][2]
          disp = (disp_y**2 + disp_x**2 + disp_z**2)
          displacements.append(disp)
    MSD = np.mean(displacements)
    displacements.clear()
    MSD_values.append(MSD)
    tau.append(j)

  fig, gr=plt.subplots()
  gr.plot(tau, MSD_values)
  gr.set_title('E.Coli MSD Graph')
  gr.set(xlabel = 'tau', ylabel = 'MSD (E-6 m^2)')
  fig.savefig('EColi_MSD.png',dpi=80)
  #combine data to a single array, transpose and save
  MSD_data = np.array([tau, MSD_values])
  MSD_data = MSD_data.T
  #savetxt('MSD_data.txt', MSD_data)

  slope,intercept = np.polyfit(tau, MSD_values, 1)
  D = slope*10/6
  print("D_eff =", D)


  #Lovely and Dahlquist comparison
  D_ld = (10*10*1)/(3*(1-0.5))
  print("Test Lovely and Dahlquist =", D_ld)


def rotate_y(alpha):
    R_y = np.array([[np.cos(alpha), 0, np.sin(alpha)],
                    [0, 1, 0],
                    [-1*np.sin(alpha), 0, np.cos(alpha)]])
    return R_y


def rotate_z(psi):
    R_z = np.array([[np.cos(psi), -1*np.sin(psi), 0],
                    [np.sin(psi), np.cos(psi), 0],
                    [0,0,1]])
    return R_z

def tumble(vector,alpha):
    new_vector = []
    vector_z = float(np.array([vector[2]]))
    vector_y = float(np.array([vector[1]]))
    vector_x = float(np.array([vector[0]]))
    r = np.sqrt(float(vector_x)**2 + float(vector_y)**2 + float(vector_z)**2)
    #print("r=", r)
    theta = np.arccos(float(vector_z)/r)
    #print("theta=", theta)
    if  (vector_x == 0):
       phi = 0
    else:
       phi = math.atan2((vector_y),(vector_x))
    rot_1 = rotate_y(alpha) @ [0,0,1]
    psi = random.uniform(0,2*np.pi)
    rot_2 = rotate_z(psi) @ (rot_1)

    new_vector = (rotate_z(phi) @ rotate_y(theta) @ rot_2)

    return new_vector
def rotate(vector):
    vector_z = float(np.array([vector[2]]))
    vector_y = float(np.array([vector[1]]))
    vector_x = float(np.array([vector[0]]))
    r = np.sqrt(float(vector_x)**2 + float(vector_y)**2 + float(vector_z)**2)

    theta = np.arccos(float(vector_z)/r)

    if  (vector_x == 0):
       phi = 0
    else:
       phi = math.atan2((vector_y),(vector_x))
    alpha = random.gauss(0, 4*0.062*0.1)
    rot_1 = rotate_y(alpha) @ [0,0,1]
    psi = random.uniform(0,2*np.pi)
    rot_2 = rotate_z(psi) @ (rot_1)

    new_vector = (rotate_z(phi) @ rotate_y(theta) @ rot_2)
    return new_vector
#Generate the number of desired steps(n) with a variable 'steps' = n+1
#Works as number of trajectories per step
trajectories, steps = (1,20000)
#Generate the starting position
x_pos,y_pos,z_pos = (0, 0, 0)

alpha=(np.pi/3)

#Generate the three arrays in which to store the coordinates
xpos_arr = []
ypos_arr = []
zpos_arr = []
#define initial vector
x=0
y=0
z=1
swim = np.array([x,
                 y,
                 z])
old_vector = np.array([x,
                       y,
                       z])
vectors = []
angles = []

#first loop
for i in range(steps):
    step = []
    #second loop is run through once per step, generating a new x, y & z vector
    #These are added to the previous values
    for j in range(trajectories):
        #Save cooridnates in respective arrays starting at origin
        xpos_arr.append(x_pos)
        ypos_arr.append(y_pos)
        zpos_arr.append(z_pos)
        swim = rotate(swim)
        #Add  vector to each position
        x_pos = x_pos + swim[0]
        y_pos = y_pos + swim[1]
        z_pos = z_pos + swim[2]
        #Reset vector to an old vector
        vectors.append(swim)
        old_vector = swim
        #Apply the tumble function to tumble 60* with a random rotation about the z axis
        tumb_test = random.random()
        if (tumb_test < 0.1):
          swim = tumble(swim,alpha)

        #dot product angle test.
        #dot = swim @ old_vector
        #angles.append(dot)

#print("angles=", angles)
#print()
#print("vectors=", vectors)
#The arrays are plotted in 3 dimensions against each other
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(xpos_arr, ypos_arr, zpos_arr)
ax.set_xlabel('X axis (um)')
ax.set_ylabel('Y axis(um)')
ax.set_zlabel('Z axis(um)')
ax.set_title("E.Coli Trajectory")
plt.savefig('EColi_Trajectory.png',dpi=80)
#Combine the arrays into a single array, transpose and save it as a .csv file.
pos_arr = np.array([xpos_arr, ypos_arr, zpos_arr])
pos_arr = pos_arr.T
np.savetxt('trajectory_file.csv', pos_arr)

Mean_Square_Disp = MSD(pos_arr)
