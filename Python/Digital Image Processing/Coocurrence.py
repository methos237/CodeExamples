# Co-occurrence Matrix on greyscale image
#
# @author James Knox Polk <jkpolk@uncg.edu>
#
# For CSC 522 - Digital Image Processing, Dr. Kim, UNCG, Spring 2019
# ===================================================================
import cv2  # used only for histogram equalization and image viewing of result
import numpy as np  # used for array and matrix operations


def coorcurr(image):
    # Build the result array
    result = np.zeros((256, 256), dtype=np.uint8)

    for x in np.arange(0, image.shape[0] - 1):
        for y in np.arange(0, image.shape[1]):
            resultx = image.item(x + 1, y)
            resulty = image.item(x, y)
            curr_value = result.item(resultx, resulty)
            result.itemset((resultx, resulty), curr_value + 1)

    return result


fd = open('source_images/cktboard.raw', 'rb')
width = 365
height = 120
f = np.fromfile(fd, dtype=np.uint8, count=height * width)
im = f.reshape((height, width))
fd.close()

imgCoocurr = coorcurr(im)
# Histogram Equalization approved by Dr. Kim
imgCoocurr_eq = cv2.equalizeHist(imgCoocurr)
imgCoocurr_eq.tofile('output_images/cktboard_texture.raw')
cv2.imshow('Grey-level Co-occurrence', imgCoocurr_eq)
cv2.waitKey(0)
cv2.destroyAllWindows()
