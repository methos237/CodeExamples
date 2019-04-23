import cv2
import numpy as np

rows = 512
cols = 512

fd = open('source_images/lena.raw', 'rb')
f = np.fromfile(fd, dtype=np.uint8, count=rows*cols)
im1 = f.reshape((rows, cols))
fd.close()

fd = open('output_images/lena_edit.raw', 'rb')
f = np.fromfile(fd, dtype=np.uint8, count=rows*cols)
im2 = f.reshape((rows, cols))
fd.close()

result = im1-im2

result.tofile('output_images/lena_subtraction.raw')
cv2.imshow('Subtraction', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
