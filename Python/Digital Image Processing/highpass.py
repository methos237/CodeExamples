import cv2
import numpy as np

rows = 512
cols = 512

fd = open('source_images/lena.raw', 'rb')
f = np.fromfile(fd, dtype=np.uint8, count=rows*cols)
im = f.reshape((rows, cols))
fd.close()
im.astype(np.float)
height = im.shape[0]
width = im.shape[1]
result = np.zeros(shape=[512, 512], dtype=np.uint8)

kernel = np.array(
    [[0, 1, 0],
     [1, -4, 1],
     [0, 1, 0]])
sum(sum(kernel))

for x in np.arange(1, height - 1):
    for y in np.arange(1, width - 1):
        sum = 0
        for k in np.arange(-1, 2):
            for l in np.arange(-1, 2):
                a = im.item(x + k, y + l)
                p = kernel[1 + k, 1 + l]
                sum = (sum + (p * a))
        b = sum / 9
        result.itemset((x, y), b)

result = im-result
result.astype(np.uint8)

result.tofile('output_images/lena_sharpened.raw')
cv2.imshow('Sharpened', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
