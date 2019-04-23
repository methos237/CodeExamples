# Image Resampling
#
# @author James Knox Polk <jkpolk@uncg.edu>
#
# For CSC 522 - Digital Image Processing, Dr. Kim, UNCG, Spring 2019
# ===================================================================

import numpy as np  # used for array and matrix operations
import cv2  # used only for histogram equalization and image viewing of result


def downsample (image):
    result = np.delete(image, list(range(0, image.shape[0], 2)), axis=0)
    result = np.delete(result, list(range(0, result.shape[1], 2)), axis=1)
    return result


def upsample (image):
    result = np.zeros((512, 512), dtype=np.uint8)

    for x in np.arange(0, image.shape[0]):
        for y in np.arange(0, image.shape[1]):
            result.itemset((x * 2, y * 2), image.item(x, y))
            result.itemset((x * 2 + 1, y * 2), image.item(x, y))
            result.itemset((x * 2, y * 2 + 1), image.item(x, y))
            result.itemset((x * 2 + 1, y * 2 + 1), image.item(x, y))

    return result


fd = open('source_images/lena.raw', 'rb')
width = 512
height = 512
f = np.fromfile(fd, dtype=np.uint8, count=height * width)
im = f.reshape((height, width))
fd.close()

result = downsample(im)

cv2.imshow('Downsampled', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

result.tofile('output_images/lena_resampling.raw')
result = upsample(result)
cv2.imshow('Upsampled', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
