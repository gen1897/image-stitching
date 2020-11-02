# image-stitching
Image stitcher using cv2.  
I am working on a version more mathematicaly based where it is easier to see how every step works.

# How does image stitching works?
- **Step 1:**
Load images.
- **Step 2:** 
Detect the keypoints in every image. This keypoints can be detected using methods such Harris or Hessian interest point detectors.
- **Step 3:** 
Compute the descriptors. Most common method is Scale-Invariant Feature Transform (SIFT).
- **Step 4:** 
Find most similar points between contiguous images. 

Once we have finished this four steps, the next steps are included in the process called RANSAC.
- **Step 5:** 
Pick a random number of similar pairs of points.
- **Step 6:**  
Compute the homography. This step will make our images have the same perspective.
- **Step 7:** 
Compute the homography distance in order to get the best homography that will make our images have the most similar perspective.  

When the RANSAC process is ended, there is only one step missing.
- **Step 8:**  
Warp images using the best homography.


# Files
## using_cv2.py
In this file images are stitching using OpenCV API. 3 functions are given:
- stitch:  
This function does the entire stitching process and returns the wrapper image. Uses ORB to detect keypoints and compute descriptors and BFMatcher to find most similar points.
The RANSAC process is intrinsic in the findHomography function. The last part in this function warps both images in one.
- check_side:  
This function finds which image is on the left side. This asserts the order of the images using stitch function.
- multi_stitch:  
If there are more than two images to be stitched together, this function warps them together.

## utils.py
Contains helper functions such as image rescaling, background cropping, etc.

## run.py
As example, stitches some images.

# Examples
This examples are made using OpenCV test images. Find them in [this OpenCV github repository](https://github.com/opencv/opencv_extra/tree/master/testdata/stitching).
Also included some examples using [this project](http://web.cecs.pdx.edu/~fliu/project/stitch/index.htm) images.
