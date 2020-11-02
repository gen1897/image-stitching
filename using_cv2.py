import numpy as np
import cv2
from utils import *


def stitch(image1: np.ndarray, image2: np.ndarray, num_matches: int = 80):
    # Convert to rgb
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Create an ORB.
    orb = cv2.ORB_create()
    # Detect keypoints and compute descriptors using orb previously created.
    kp1, des1 = orb.detectAndCompute(image1_gray, None)
    kp2, des2 = orb.detectAndCompute(image2_gray, None)

    # Create a matcher to find most similarity between descriptors.
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    # Sort matches by similarity (Descendent order).
    matches = sorted(matches, key=lambda x: x.distance)
    if num_matches != 0:
        matches = matches[:num_matches]

    MIN_MATCH = 9

    if len(matches) > MIN_MATCH:
        # Convert keypoints to numpy
        src_pts = np.float32(
            [kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32(
            [kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        # Find Homography
        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 4.0)
    else:
        print("Not enought matches are found - %d/%d",
              (len(matches)/MIN_MATCH))

    # Warp images in one.
    dst = cv2.warpPerspective(
        image1, M, (image2.shape[1] + image1.shape[1], image2.shape[0]))
    dst[0:image2.shape[0], 0:image2.shape[1]] = image2

    return dst


def check_side(image1, image2):
    # Make stitching with both images
    stitch1 = stitch(image1, image2)
    stitch2 = stitch(image2, image1)
    # Transform to gray scale both images
    image1_gray = cv2.cvtColor(stitch1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(stitch2, cv2.COLOR_BGR2GRAY)
    # Count pixels with 0's in each image. The one with more is the one who hasn't been stitched
    image1_zeros = cv2.countNonZero(image1_gray)
    image2_zeros = cv2.countNonZero(image2_gray)
    # Return image that has less black
    if image1_zeros > image2_zeros:
        return stitch1
    else:
        return stitch2


def multi_stitch(images):
    # Make a list with all images from right to left
    inv_images = [cv2.imread(image) for image in reversed(images)]
    # Select image on the right as starter point
    stitched_image = inv_images[0]
    # Stitch images in a loop right to left
    for index in range(1, len(inv_images)):
        stitched_image = check_side(stitched_image, inv_images[index])

    return stitched_image
