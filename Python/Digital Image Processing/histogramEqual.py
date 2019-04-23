import numpy as np
import cv2
import math

rows = 512
cols = 512

fd = open('source_images/lena.raw', 'rb')
f = np.fromfile(fd, dtype=np.uint8, count=rows*cols)
im = f.reshape((rows, cols))
fd.close()

result = im.copy()


def histogram(img):
    img_height = img.shape[0]
    img_width = img.shape[1]

    hist_result = np.zeros(256)

    for i in np.arange(img_height):
        for j in np.arange(img_width):
            a = img.item(i, j)
            hist_result[a] += 1

    for i in np.arange(1, 256):
        hist_result[i] = hist_result[i - 1] + hist_result[i]

    return hist_result


height = im.shape[0]
width = im.shape[1]
pixels = width * height

hist = histogram(im)

for i in np.arange(height):
    for j in np.arange(width):
        a = im.item(i, j)
        b = math.floor(hist[a] * 255.0 / pixels)
        result.itemset((i, j), b)

result.tofile('output_images/lena_histequal.raw')

cv2.imshow('Equalized', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
