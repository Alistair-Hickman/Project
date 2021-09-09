# Project
Trajectory Creation:
I believe most parameters are self explanatory including the total simulation time, frequency of position capture. 
The mean run and stop times can be adjusted as desired (these are done in seconds).

The "Correction", "Steps", "stop_steps" & "run_steps" should not be adjusted and are all dependant on the other parameters.
None of the functions should need changing for any runs.

The initial coordinates of the bugs is controlled through the x,y and z _init variables. These are done in microns from -x to +x. 
This range should be equal to the desired sample volume of the final image so the bugs are 'equally' distributed across the sample.

Finally set the 'path' variable to the desired file location on your machine. The str(l) term allows the creation of multiple trajectories 
with different numbers. Make sure to include this in whatever file path you choose. Other than this do not alter the DataFrame (df) or df.to_csv.

Nothing beyond this should require changing in the code for it to produce the desired trajectories.

Image Creation Script:
This code is slightly more complex but flexible. 
'No_bugs' is self explanatory.
'No_frames' is the maximum trajectory step, not the actual number of frames if the spacing between frame is not 1. The number of frames that will be produced
is no_frames/frame_spacing.

'P', 'q' and 'sigma' are the variables that will effect the intensity of the pixel values. P and q relate to the z position in the form of p*z*z + q. P should be a 
negative coefficient which governs the depth of field in the image, i.e the vertical range in which the bugs will be visible, this will typically vary between
-0.1 and -0.0001. The depth in microns can be calculated by hand using the quadratic above by finding the value at which it <= 0.

Sigma corresponds to the Gaussian function which governs the intensity at any radius r from the bug itself, this will typically vary between 1.0-5.0. This is a 
little less scientific, the best value can just be found through creating images and seeing what looks good. Perfection isn't particularly necessary, just good enough.

'x' and 'y' are the pixel ranges of the image, 'width' is the image volume width in microns.

This script requires to file locations to be set:
The first is in the im.save() term, set this to the file in which the frames will be saved. Again keep the str(ii) term for the frames to be numbered.

Near the bottom of the script merely set the 'open_path' to the same 'path' you used for the trajectories to be saved. Nothing else needs to be changed, 
do not change any of the data frame variables or names.

A final note on the mp.Process. This allows some parallelisation in Python but as far as I know it only works when python is run through the terminal. 
If this proves to be problematic I believe the script can be run by just calling the "main_loop" function and deleting this process call.


