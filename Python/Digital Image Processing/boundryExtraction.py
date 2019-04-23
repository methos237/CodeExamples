import cv2  # used only for image viewing of result
import numpy as np  # used for array and matrix operations


# Takes binary input image and dilates or erodes based on threshold input using a 3x3 SE of 9 1's
# To dilate, input a threshold of 0, to erode a threshold of 255
# Returns the dilated or eroded image array
def np_binary_ero_dil(input_array, threshold):
    result = np.zeros(input_array.shape, dtype=np.uint8)
    goal = 255 if threshold == 0 else 0

    # pad the array to fit the kernel, this way the entire image is processed
    np.pad(input_array, ((1, 1), (1, 1)), 'edge')

    for x in np.arange(1, input_array.shape[0] - 1):
        for y in np.arange(1, input_array.shape[1] - 1):
            if input_array.item(x - 1, y + 1) == threshold and input_array.item(x, y + 1) == threshold \
                    and input_array.item(x + 1, y + 1) == threshold and input_array.item(x - 1, y) == threshold \
                    and input_array.item(x, y) == threshold and input_array.item(x + 1, y) == threshold \
                    and input_array.item(x - 1, y - 1) == threshold and input_array.item(x, y - 1) == threshold \
                    and input_array.item(x + 1, y - 1) == threshold:
                result.itemset((x, y), im.item(x, y))
            else:
                result.itemset((x, y), goal)
    return result


fd = open('source_images/lincoln.raw', 'rb')
height = 269
width = 221
f = np.fromfile(fd, dtype=np.uint8, count=height * width)
im = f.reshape((height, width))
fd.close()

# First generate an erosion from the source image
eroResult = np_binary_ero_dil(im, 255).astype(np.uint8)

# Subtract the eroded image from the source for the boundary extraction
extractResult = im-eroResult
extractResult.tofile('output_images/lincoln_boundary.raw')
cv2.imshow('Boundary Extraction', extractResult)
cv2.waitKey(0)
cv2.destroyAllWindows()
