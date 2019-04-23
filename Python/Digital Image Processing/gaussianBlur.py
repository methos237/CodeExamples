import cv2
import numpy as np

rows = 512
cols = 512

fd = open('source_images/lena.raw', 'rb')
f = np.fromfile(fd, dtype=np.uint8, count=rows*cols)
im = f.reshape((rows, cols))
fd.close()

height = im.shape[0]
width = im.shape[1]
result = im.copy()

kernel = (1.0 / 57) * np.array(
    [[0, 1, 2, 1, 0],
     [1, 3, 5, 3, 1],
     [2, 5, 9, 5, 2],
     [1, 3, 5, 3, 1],
     [0, 1, 2, 1, 0]])
sum(sum(kernel))

for x in np.arange(2, height - 2):
    for y in np.arange(2, width - 2):
        sum = 0
        for k in np.arange(-2, 3):
            for l in np.arange(-2, 3):
                a = im.item(x + k, y + l)
                p = kernel[2 + k, 2 + l]
                sum = sum + (p * a)
        b = sum
        result.itemset((x, y), b)

result = result.astype(np.uint8)
result.tofile('output_images/lena_smooth.raw')
cv2.imshow('Smoothed', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
