from PIL import Image
from skimage.feature import canny
from skimage.draw import line
from skimage.morphology import skeletonize
from skimage.filters import threshold_otsu
from skimage import img_as_ubyte
import numpy as np
from FindLines import find_lines
from hough_split import hough_split
import math
from pathlib import Path
import time
import matplotlib.pyplot as plt


def find_errors(filename, reduce_rate=0, otsu=1, high=.9, low=.4, sigma=1):
    total_time = time.time()
    path = Path(filename)
    print(str(path))
    open_time = time.time()
    image = Image.open(filename).convert("L")
    image = np.array(image)
    print('open time: ' + str(time.time() - open_time))
    im_shape = np.shape(image)
    print(im_shape)

    # image = img_as_ubyte(image)
    # image = image[0:im_shape[0]/10, 0:im_shape[1]/10]
    # im_shape = np.shape(image)
    # print(im_shape)
    if reduce_rate:
        image = np.multiply(np.floor(np.divide(image, 2**reduce_rate)), 2**reduce_rate)

    print('start processing')

    if otsu:
        otsu_time = time.time()
        thresh = threshold_otsu(image)
        print('done otsu')
        print('otsu time: ' + str(time.time() - otsu_time))

        canny_time = time.time()
        canny_edges = np.array(canny(image, sigma, low*thresh, high*thresh))
        print('done canny')
        print('canny time: ' + str(time.time() - canny_time))
    else:
        print('?')
        canny_edges = canny(image, sigma, low, high)

    # plt.imshow(canny_edges)
    # plt.show()

    # np.save("C:\\Malachite\\saved-split\\line_report_" + path.stem + "_edges.npy", edges)

    hough_split_time = time.time()
    hough_lines = hough_split(canny_edges, 50, im_shape, 0)
    np.save("C:\\Malachite\\saved-split\\twice_" + path.stem + "_all-hough-lines.npy", np.array(hough_lines))
    print('done hough split')
    print('hough split time: ' + str(time.time() - hough_split_time))

    # hough_time = time.time()
    # lines = probabilistic_hough_line(edges, 10, 30)
    # print('done hough')
    # print('hough time: ' + str(time.time() - hough_time))

    # TO SAVE LINES
    long_hough_lines = []
    for x, l in enumerate(hough_lines):
        p0, p1 = l
        if math.fabs(math.sqrt(math.pow((p1[1]-p0[1]), 2)+math.pow((p1[0]-p0[0]), 2))) > 10:
            long_hough_lines.append(l)
    np.save("C:\\Malachite\\saved-split\\twice_" + path.stem + "_hough-lines.npy", np.array(long_hough_lines))

    plot_time = time.time()
    hough_plot = np.zeros(im_shape, bool)
    for l in hough_lines:
        p0, p1 = l
        rr, cc = line(int(p0[0]), int(p0[1]), int(p1[0]), int(p1[1]))
        hough_plot[rr, cc] = True

    # plt.imshow(hough_plot)
    # plt.show()

    print('done hough plot')
    print('hough plot time: ' + str(time.time() - plot_time))

    and_time = time.time()
    result_image = np.logical_and(canny_edges, hough_plot)

    thin_result_lines = skeletonize(result_image)
    found_result_lines = find_lines(thin_result_lines)
    print('done AND')
    print('AND time:' + str(time.time() - and_time))

    length_time = time.time()
    long_result_lines = []
    for l in found_result_lines:
        p0, p1 = l
        if p0[0] > p1[0]:
            l = (p1, p0)
        if math.sqrt(math.pow((p1[1]-p0[1]), 2)+math.pow((p1[0]-p0[0]), 2)) > 10:
            long_result_lines.append(l)

    error_time = time.time()
    result_plot = np.zeros(im_shape, bool)
    for l in long_result_lines:
        p0, p1 = l
        rr, cc = line(int(p0[1]), int(p0[0]), int(p1[1]), int(p1[0]))
        result_plot[rr, cc] = True
    error_image = np.logical_xor(result_plot, hough_plot)
    thin_error_lines = skeletonize(error_image)
    found_error_lines = find_lines(thin_error_lines)
    print('done error')
    print('error time:' + str(time.time() - error_time))
    # plt.imshow(result_plot)
    # plt.show()

    long_error_lines = []
    for l in found_error_lines:
        p0, p1 = l
        if p0[0] > p1[0]:
            l = (p1, p0)
        if math.sqrt(math.pow((p1[1]-p0[1]), 2)+math.pow((p1[0]-p0[0]), 2)) > 5:
            long_error_lines.append(l)
    print('length time - ignore this: ' + str(time.time() - length_time))
    np.save("C:\\Malachite\\saved-split\\twice_" + path.stem + "_result-lines.npy", np.array(long_result_lines))
    np.save("C:\\Malachite\\saved-split\\twice_" + path.stem + "_error-lines.npy", np.array(long_error_lines))

    with open("C:\\Malachite\\saved-split\\line_report_" + path.stem + "_" + str(high) + "_" + str(low) + ".txt", "w") as f:
        f.write("Line, Heading, Length")
        for x, l in enumerate(long_result_lines):
            p0, p1 = l
            string = [str(x), ", ", str(math.degrees(math.atan2((p0[0] - p1[0]), (p0[1] - p1[1])))), ", ",
                      str(math.sqrt(math.pow((p1[1] - p0[1]), 2) + math.pow((p1[0] - p0[0]), 2))), "\n"]
            # string.insert(1, str(p0))
            # string.insert(3, str(p1))
            # string.insert(5, str(math.sqrt(math.pow((p1[1]-p0[1]), 2)+math.pow((p1[0]-p0[0]), 2))))
            # string.insert(7, str(math.degrees(math.atan2(p0[1] - p1[1], p1[0] - p0[0]))))
            f.write("".join(string))

    with open("C:\\Malachite\\saved-split\\line_report_error_" + path.stem + "_" + str(high) + "_" + str(low) + ".txt", "w") as f:
        f.write("Line, Heading, Length")
        for x, l in enumerate(long_error_lines):
            p0, p1 = l
            string = [str(x), ", ", str(math.degrees(math.atan2((p0[0] - p1[0]), (p0[1] - p1[1])))), ", ",
                      str(math.sqrt(math.pow((p1[1] - p0[1]), 2) + math.pow((p1[0] - p0[0]), 2))), "\n"]
            f.write("".join(string))

    print('done find errors')
    print('full time: ' + str(time.time() - total_time))

    return long_result_lines
