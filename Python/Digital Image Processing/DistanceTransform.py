# Distance Transformation on binary image
#
# @author James Knox Polk <jkpolk@uncg.edu>
#
# For CSC 522 - Digital Image Processing, Dr. Kim, UNCG, Spring 2019
# ===================================================================
import cv2  # used only for histogram equalization
import numpy as np  # used for array and matrix operations


def distance_transform(image):
    # Set all non-zero values to a high number
    image[image > 0] = 3000

    # Do first pass through array (left to right, top to bottom)
    # and set x, y to the minimum of the 4d neighbors + 1
    for x in np.arange(1, image.shape[0]-1):
        for y in np.arange(1, image.shape[1]-1):
            if image.item(x, y) != 0:
                a = image.item(x - 1, y) + 1
                b = image.item(x + 1, y) + 1
                c = image.item(x, y - 1) + 1
                d = image.item(x, y + 1) + 1
                image.itemset((x, y), min(a, b, c, d))

    # Do second pass through array (right to left, bottom to top)
    # and set x, y to the minimum of the 4d neighbors + 1
    for x in np.arange(image.shape[0]-1, 1, -1):
        for y in np.arange(image.shape[1]-1, 1, -1):
            if image.item(x, y) != 0:
                a = image.item(x - 1, y) + 1
                b = image.item(x + 1, y) + 1
                c = image.item(x, y - 1) + 1
                d = image.item(x, y + 1) + 1
                image.itemset((x, y), min(a, b, c, d))

    return image


fd = open('source_images/square.raw', 'rb')
height = 60
width = 60
f = np.fromfile(fd, dtype=np.uint8, count=height * width)
im = f.reshape((height, width))
fd.close()

result = distance_transform(im)
# Histogram Equalization approved by Dr. Kim
result = cv2.equalizeHist(result)
result.tofile('output_images/square_disttrans.raw')
cv2.imshow('Distance Transformation', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
