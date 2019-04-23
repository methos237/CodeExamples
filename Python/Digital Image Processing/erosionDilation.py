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


# Open the source image and convert to a numpy array
fd = open('source_images/fingerprint.raw', 'rb')
height = 238
width = 315
f = np.fromfile(fd, dtype=np.uint8, count=height * width)
im = f.reshape((height, width))
fd.close()

# Process the dilation
dilResult = np_binary_ero_dil(im, 0).astype(np.uint8)
dilResult.tofile('output_images/fingerprint_dilation.raw')
cv2.imshow('Dilation', dilResult)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Process the erosion
eroResult = np_binary_ero_dil(im, 255).astype(np.uint8)
eroResult.tofile('output_images/fingerprint_erosion.raw')
cv2.imshow('Erosion', eroResult)
cv2.waitKey(0)
cv2.destroyAllWindows()
