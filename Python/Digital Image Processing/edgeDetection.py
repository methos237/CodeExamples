from math import sqrt
import numpy as np  # used for array and matrix operations


def derivx(image):
    result = np.zeros(image.shape, dtype=np.int16)
    # pad the array to fit the kernel, this way the entire image is processed
    np.pad(image, ((0, 0), (1, 1)), 'edge')

    for x in np.arange(0, image.shape[0] - 1):
        for y in np.arange(0, image.shape[1]):
            # get the first order x derivative
            diff = image.item(x + 1, y) - image.item(x, y)
            result.itemset((x, y), diff)

    return result


def derivy(image):
    result = np.zeros(image.shape, dtype=np.int16)
    # pad the array to fit the kernel, this way the entire image is processed
    np.pad(image, ((1, 1), (0, 0)), 'edge')

    for x in np.arange(0, image.shape[0]):
        for y in np.arange(0, image.shape[1] - 1):
            # get the first order y derivative
            diff = image.item(x, y + 1) - image.item(x, y)
            result.itemset((x, y), diff)
    return result


def gradient(image):
    result = np.zeros(image.shape, dtype=np.int16)
    grad_x = derivx(image)
    grad_y = derivy(image)

    for x in np.arange(0, image.shape[0]):
        for y in np.arange(0, image.shape[1]):
            # Get the magnitude of the image
            calc = sqrt((grad_x.item(x, y) ** 2) + (grad_y.item(x, y) ** 2))
            result.itemset((x, y), abs(calc))

    return result


fd = open('source_images/lena.raw', 'rb')
height = 512
width = 512
f = np.fromfile(fd, dtype=np.uint8, count=height * width)
im = f.reshape((height, width))
im.astype(np.int)
fd.close()

derivxResult = derivx(im)
derivxResult.tofile('output_images/lena_derivX.raw')

derivyResult = derivy(im)
derivyResult.tofile('output_images/lena_derivY.raw')

gradientResult = gradient(im)
gradientResult.tofile('output_images/lena_gradient.raw')
