import numpy as np
from numpy.random import seed
import random
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math
from numpy import savetxt
import pandas as pd

Particles = 200

for l in range(Particles):

 MSD_results = []
 MAD_results = []
 Time = []

 time_tot = 5*60 #Total sim time in seconds
 #Run speed in microns/second
 run_speed = 20.0
 #Corresponding frequency-needs to be 100Hz
 freq = 100.0
 Correction = run_speed/freq
 #Total steps
 steps = time_tot*freq
 #mean stop duration in seconds and corresponding variables
 mean_stop =  1.0
 stop_steps = mean_stop * freq
 stop_lambd = 1.0/stop_steps
 #mean run time in seconds and corresponding variables
 mean_run = 3.0
 run_steps = mean_run * freq
 run_lambd = 1.0/run_steps

 no_runs = int(time_tot/(mean_run + mean_stop))
 #Mean Square Displacement Fucntion

 def MSD(pos_arr):
  MSD_values = []
  displacements = []
  tau = []

 def MAD(angles):
   MAD_values = []
   ang_displacements = []

   for i in range(1, len(angles)):
     ang_sq = angles[i] * angles[i]
     ang_displacements.append(ang_sq)
   MSAD = np.mean(ang_displacements)
   return MSAD

 #Rotate about the y axis
 def rotate_y(alpha):
     R_y = np.array([[np.cos(alpha), 0, np.sin(alpha)],
                    [0, 1, 0],
                    [-1*np.sin(alpha), 0, np.cos(alpha)]])
     return R_y

#ROtate about the z axis
 def rotate_z(psi):
     R_z = np.array([[np.cos(psi), -1*np.sin(psi), 0],
                    [np.sin(psi), np.cos(psi), 0],
                    [0,0,1]])
     return R_z
 #Overall rotte function, calls both functions above.
 def rotate(vector):
    #Definition of variables within function
    vector_z = float(np.array([vector[2]]))
    vector_y = float(np.array([vector[1]]))
    vector_x = float(np.array([vector[0]]))
    r = np.sqrt(float(vector_x)**2 + float(vector_y)**2 + float(vector_z)**2)
    #Spherical coordinate theta definition
    theta = np.arccos(float(vector_z)/r)
    #Spherical coordinate Phi definition
    if  (vector_x == 0):
       phi = 0
    else:
       phi = math.atan2((vector_y),(vector_x))
    #Alpha is angle rotated away from current axis, calculated randomly in every instance
    #CHANGE FOR FREQ CHANGE
    alpha = random.gauss(0, 4*0.062*0.01)
    #Call first rotation matrix with random alpha
    #and multiply to 0,0,1 vector
    rot_1 = rotate_y(alpha) @ [0,0,1]
    #Calculate random angle to rotate about previous vector
    psi = random.uniform(0,2*np.pi)
    #Apply this rotation with the calculated Psi angle
    #onto the rotation already applied
    rot_2 = rotate_z(psi) @ (rot_1)
    #Final calculation of new direction by taking the final vector from above
    #and rotate the reference frame onto the new vector using theta and phi.
    #This allows all the initial rotations to be applied to 0,0,1
    new_vector = (rotate_z(phi) @ rotate_y(theta) @ rot_2)

    return new_vector

 def initial_stop(swim):
    duration = int(10*freq)
    swim = np.array([x,y,z])
    for i in range(duration):
        swim = stop_rotate(swim)
    return swim


 def stop(swim):
    #Stop duration in uniform between 0.5-1.5s
    stop_duration = random.expovariate(stop_lambd)
    #Needs int rounding but allows stop duration to nearest 0.01s. Okay, could be better
    int_stop = int(stop_duration)
    for i in range(int_stop):
        xpos_arr.append(x_pos)
        ypos_arr.append(y_pos)
        zpos_arr.append(z_pos)
        swim = stop_rotate(swim)
        vectors.append(swim)
    return swim

 def stop_rotate(vector):
    #Definition of variables within function
    vector_z = float(np.array([vector[2]]))
    vector_y = float(np.array([vector[1]]))
    vector_x = float(np.array([vector[0]]))
    r = np.sqrt(float(vector_x)**2 + float(vector_y)**2 + float(vector_z)**2)
    #Spherical coordinate theta definition
    theta = np.arccos(float(vector_z)/r)
    #Spherical coordinate Phi definition
    if  (vector_x == 0):
       phi = 0
    else:
       phi = math.atan2((vector_y),(vector_x))
    #Alpha is angle rotated away from current axis, calculated randomly in every instance
    #CHANGE FOR FREQ
    alpha = random.gauss(0, 4*0.12*0.01)
    #Call first rotation matrix with random alpha
    #and multiply to 0,0,1 vector
    rot_1 = rotate_y(alpha) @ [0,0,1]
    #Calculate random angle to rotate about previous vector
    psi = random.uniform(0,2*np.pi)
    #Apply this rotation with the calculated Psi angle
    #onto the rotation already applied
    rot_2 = rotate_z(psi) @ (rot_1)
    #Final calculation of new direction by taking the final vector from above
    #and rotate the reference frame onto the new vector using theta and phi.
    #This allows all the initial rotations to be applied to 0,0,1
    new_vector = (rotate_z(phi) @ rotate_y(theta) @ rot_2)

    return new_vector

 #Generate the number of desired steps(n) with a variable 'steps' = n+1
 #Works as number of trajectories per step
 x_init = random.uniform(-50,50)
 z_init = random.uniform(-50,50)
 #Generate the starting position
 x_pos,y_pos,z_pos = (x_init, z_init, 0)

 #Generate the three arrays in which to store the coordinates
 xpos_arr = []
 ypos_arr = []
 zpos_arr = []
 #define initial vector
 x=0
 y=0
 z=random.choice([-1,1])
 swim = np.array([x,
                 y,
                 z])
 swim = initial_stop(swim)

 old_vector = np.array([x,
                       y,
                       z])
 vectors = []
 angles = []

 #first loop
 for i in range(no_runs):
    step = []
    #second loop is run through once per step, generating a new x, y & z vector
    #These are added to the previous values
    run_time = random.expovariate(run_lambd)
    int_run = int(run_time)
    for k in range(int_run):
        #Save cooridnates in respective arrays starting at origin
        xpos_arr.append(x_pos)
        ypos_arr.append(y_pos)
        zpos_arr.append(z_pos)
        #Add  vector to each position
        x_pos = x_pos + swim[0]*Correction
        y_pos = y_pos + swim[1]*Correction
        z_pos = z_pos + swim[2]*Correction
        #Reset vector to an old vector
        vectors.append(swim)
        #Apply the tumble function to tumble 60* with a random rotation about the z axis
        swim = rotate(swim)
        old_vector = swim
    swim = stop(swim)
    dot = swim @ old_vector
    angles.append(dot)

 #The arrays are plotted in 3 dimensions against each other
 ax = plt.axes(projection='3d')
 ax.plot3D(xpos_arr, ypos_arr, zpos_arr)
 ax.set_xlabel('X axis(um)')
 ax.set_ylabel('Y axis(um)')
 ax.set_zlabel('Z axis(um)')
 ax.set_title("R.Spheroides Trajectory")
 plt.savefig("R.Sphaeroides_trajectory.png",dpi=80)

 #Combine the arrays into a single array, transpose and save it as a .csv file.
 #times = 0.00
 #for i in range(len(xpos_arr)):
     #times += 0.01
     #Time.append(times)
 pos_arr = np.array([xpos_arr, ypos_arr, zpos_arr])
 pos_arr = pos_arr.T
 df = pd.DataFrame(pos_arr, columns = ["X", "Y", "Z"])
 path = "/Users/alistair/Documents/Project/Scripts/Trajectories2.nosync/trajectory_" + str(l) + ".csv"
 df.to_csv(path, sep = "\t")

 #Mean_S_Ang_Disp=MAD(angles)
 #Mean_Ang_Disp=np.sqrt(Mean_S_Ang_Disp)
 #print("MAD=", Mean_Ang_Disp)

 #v_avrg = (run_speed*mean_run)/(mean_run+mean_stop/run_speed)
 #D_ld = (v_avrg*v_avrg*(mean_run+(mean_stop/run_speed)))/(3*(1-np.cos(Mean_Ang_Disp)))
 #print("D_ld=", D_ld)

 MAD_results.clear()
 MSD_results.clear()
 Time.clear()
