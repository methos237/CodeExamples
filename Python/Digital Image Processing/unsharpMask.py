import cv2
import numpy as np

rows = 512
cols = 512

fd = open('source_images/lena.raw', 'rb')
f = np.fromfile(fd, dtype=np.uint8, count=rows*cols)
im1 = f.reshape((rows, cols))
fd.close()

fd = open('source_images/lena_smooth.raw', 'rb')
f = np.fromfile(fd, dtype=np.uint8, count=rows*cols)
im2 = f.reshape((rows, cols))
fd.close()

im3 = im1-im2
result = im1+im3

result.tofile('output_images/lena_unsharpmask.raw')
cv2.imshow('Unsharp Masking', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
