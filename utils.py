import cv2
import numpy as np
import os


def show_image(image):
    # Show image
    cv2.imshow("image", image)
    # Freeze untill a key is pressed
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()


def rescale(or_height: int, image):
    # Relationship between new and old height
    scalator = (image.shape[1] / or_height)
    # Set new dimensions
    dim = (int(image.shape[1]/scalator), int(image.shape[0]/scalator))
    # CV2 resize
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return resized


def check_images(keyword: str):
    # Empty list.
    images = []
    # Fill list the name of images that contain the keyword
    for dirname, _, filenames in os.walk('input'):
        for filename in filenames:
            image = os.path.join(dirname, filename)
            if keyword in image:
                images.append(image)
    return images


def autocrop(image, threshold=0):
    # RGB
    if len(image.shape) == 3:
        flatImage = np.max(image, 2)
    # Gray
    else:
        flatImage = image
    assert len(flatImage.shape) == 2
    # Select only rows the rows that are not completely black
    rows = np.where(np.max(flatImage, 0) > threshold)[0]
    if rows.size:
        cols = np.where(np.max(flatImage, 1) > threshold)[0]
        image = image[cols[0]: cols[-1] + 1, rows[0]: rows[-1] + 1]
    else:
        image = image[:1, :1]

    return image


def save_image(image, name: str):
    cv2.imwrite(("output/{}.jpg".format(name)), image)
