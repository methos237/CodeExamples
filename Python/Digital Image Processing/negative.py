import numpy as np
import cv2

rows = 512
cols = 512

fd = open('source_images/lena.raw', 'rb')
f = np.fromfile(fd, dtype=np.uint8, count=rows*cols)
im = f.reshape((rows, cols))
fd.close()

result = im.copy()

for x in range(0, im.shape[0]):
    for y in range(0, im.shape[1]):
        result[x, y] = (255-im[x, y])

result.tofile('output_images/lena_negative.raw')
cv2.imshow('Negative', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
