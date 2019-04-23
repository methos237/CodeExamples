# Correlation Coefficient Similarity Map
#
# @author James Knox Polk <jkpolk@uncg.edu>
#
# For CSC 522 - Digital Image Processing, Dr. Kim, UNCG, Spring 2019
# ===================================================================

import numpy as np  # used for array and matrix operations
import cv2  # used only for image viewing of result
import math
import timeit as tit


def normalize_image(im):
    w, h = im.shape
    minval = np.amin(im)
    if minval < 0:
        im = im + abs(minval)
    maxval = np.amax(im)
    nm_result = np.zeros(im.shape, 'd')
    for x in np.arange(0, w):
        for y in np.arange(0, h):
            nm_result.itemset((x, y), float(im.item(x, y)) / maxval)

    return nm_result


def correlation_coeff(source, template):
    t = tit.Timer()

    c_result = np.zeros(source.shape)
    s_width, s_height = source.shape
    t_width, t_height = template.shape
    t_mean = np.mean(template)
    print("Computing Correleation Coefficients...")
    start_time = t.timer()

    for i in np.arange(0, s_width):
        for j in np.arange(0, s_height):
            # Create a sub-image slice to compare with template
            if i - t_width / 2 <= 0:
                left = 0
            elif s_width - i < t_width:
                left = s_width - t_width
            else:
                left = i

            right = left + t_width

            if j - t_height / 2 <= 0:
                top = 0
            elif s_height - j < t_height:
                top = s_height - t_height
            else:
                top = j

            bottom = top + t_height

            sub = source[left:right, top:bottom]
            sub_mean = np.mean(sub)
            temp = (sub - sub_mean) * (template - t_mean)
            s1 = temp.sum()
            temp = (sub - sub_mean) * (sub - sub_mean)
            s2 = temp.sum()
            temp = (template - t_mean) * (template - t_mean)
            s3 = temp.sum()
            denom = s2 * s3
            if denom == 0:
                temp = 0
            else:
                temp = s1 / math.sqrt(denom)

            c_result.itemset((i, j), temp)

    end_time = t.timer()
    print("=> Correlation computed in: ", end_time - start_time)

    return c_result


fd = open('source_images/flowers.raw', 'rb')
width = 400
height = 300
f = np.fromfile(fd, dtype=np.uint8, count=height * width)
im_r = f.reshape((height, width))
fd.close()

fd = open('source_images/flowers-template.raw', 'rb')
width = 42
height = 45
f = np.fromfile(fd, dtype=np.uint8, count=height * width)
im_t = f.reshape((height, width))
fd.close()


corr = correlation_coeff(im_r, im_t)
result = normalize_image(corr) * 255
result = result.astype(np.uint8)

result.tofile('output_images/flowers_correlation_coefficient.raw')

cv2.imshow('Correlation Coefficient Map', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
