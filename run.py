from utils import *
from using_cv2 import *


def main():
    IMAGE_NAME = "cartel"

    # Load images
    images = check_images(IMAGE_NAME)

    # Stitch images
    image = multi_stitch(images)

    # Rescale image
    rescaled_image = autocrop(rescale(1000, image))

    # Show image
    # show_image(image)

    # Save image as jpg
    save_image(rescaled_image, IMAGE_NAME)


if __name__ == "__main__":
    main()
