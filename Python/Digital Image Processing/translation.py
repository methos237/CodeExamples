import numpy as np
import cv2

rows = 512
cols = 512

fd = open('source_images/lena.raw', 'rb')
f = np.fromfile(fd, dtype=np.uint8, count=rows*cols)
im = f.reshape((rows, cols))
fd.close()

result = np.zeros(shape=[512, 512], dtype=np.uint8)

for x in range(0, im.shape[0]):
    for y in range(0, im.shape[1]):
        if x <= 512-6:
            if y <= 512-6:
                result[x+5, y+5] = (im[x, y])

result.tofile('output_images/lena_translation.raw')
cv2.imshow('Translation', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
