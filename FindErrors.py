from PIL import Image
from skimage.transform import probabilistic_hough_line
from skimage.feature import canny
from skimage.draw import line
from skimage.morphology import skeletonize
from skimage.filters import threshold_otsu
from skimage import img_as_ubyte
import numpy as np
from FindLines import find_lines
import math
from pathlib import Path


def find_errors(filename, reduce_rate=0, otsu=1, high=.9, low=.4, sigma=1):
    path = Path(filename)
    image = Image.open('/Volumes/Untitled/10bcd15202_651_30_8bit_rgbiR.tif').convert("L")
    image = np.array(image)
    im_shape = np.shape(image)

    image = img_as_ubyte(image)
    if reduce_rate:
        image = np.multiply(np.floor(np.divide(image, 2**reduce_rate)), 2**reduce_rate)

    if otsu:
        thresh = threshold_otsu(image)
        edges = canny(image, sigma, low*thresh, high*thresh)
    else:
        edges = canny(image, sigma, low, high)

    print('done canny')

    lines = probabilistic_hough_line(edges, 10, 30)

    print('done hough')

    line_plot = np.zeros(im_shape, bool)
    for l in lines:
        p0, p1 = l
        rr, cc = line(p0[1], p0[0], p1[1], p1[0])
        line_plot[rr, cc] = True

    print('done hough plot')

    line_and_edge = np.zeros(im_shape, bool)
    for rr in range(0, im_shape[0]):
        for cc in range(0, im_shape[1]):
            line_and_edge[rr, cc] = edges[rr, cc] and line_plot[rr, cc]

    print('done AND')

    thin_lines = skeletonize(line_and_edge)
    filtered_lines = find_lines(thin_lines)

    print('done find lines')

    long_lines = []
    for l in filtered_lines:
        p0, p1 = l
        if p0[1] > p1[1]:
            l = (p1, p0)
        if math.sqrt(math.pow((p1[0]-p0[0]), 2)+math.pow((p1[1]-p0[1]), 2)) > 10:
            long_lines.append(l)

    with open("/Volumes/Untitled/reports/line_report_" + path.stem + "_" + str(high) + "_" + str(low) + ".txt", "w") as f:
        for l in long_lines:
            p0, p1 = l
            string = ["P1: ", ", P2: ", ", Length: ", ", Heading: ", "\n"]
            string.insert(1, str(p0))
            string.insert(3, str(p1))
            string.insert(5, str(math.sqrt(math.pow((p1[0]-p0[0]), 2)+math.pow((p1[1]-p0[1]), 2))))
            string.insert(7, str(math.degrees(math.atan2(p0[0] - p1[0], p1[1] - p0[1]))))
            f.write("".join(string))

    return long_lines
