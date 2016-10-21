import numpy as np
from scipy.ndimage.filters import convolve
from collections import deque


def find_lines(img):
    print('finding.........')
    lines = []
    weights = [[1, 1, 1],
               [1, 10, 1],
               [1, 1, 1]]
    weighted_image = convolve(img.astype(int), weights)
    weighted_image *= (weighted_image > 10)
    endpoint_queue = deque(np.argwhere(weighted_image == 11))
    while endpoint_queue:
        start_point = endpoint_queue.pop()
        if weighted_image[start_point[0], start_point[1]] != 11:
            continue
        working_point = start_point
        final_point = False
        while not final_point:
            weighted_image[working_point[0], working_point[1]] = 0
            c = (weighted_image[working_point[0] - 1:working_point[0] + 2, working_point[1] - 1:working_point[1] + 2])
            p = np.flatnonzero(c)
            if p:
                p = p[0]
            else:
                break
            if p == 0:
                working_point = (working_point[0] - 1, working_point[1] - 1)
            elif p == 1:
                working_point = (working_point[0] - 1, working_point[1])
            elif p == 2:
                working_point = (working_point[0] - 1, working_point[1] + 1)
            elif p == 3:
                working_point = (working_point[0], working_point[1] - 1)
            elif p == 5:
                working_point = (working_point[0], working_point[1] + 1)
            elif p == 6:
                working_point = (working_point[0] + 1, working_point[1] - 1)
            elif p == 7:
                working_point = (working_point[0] + 1, working_point[1])
            elif p == 8:
                working_point = (working_point[0] + 1, working_point[1] + 1)
            if weighted_image[working_point[0], working_point[1]] == 11:
                weighted_image[working_point[0], working_point[1]] = 0
                final_point = True
                continue
            if (weighted_image[working_point[0], working_point[1]]) != 12:
                break
        else:
            r = ((start_point[1], start_point[0]), (working_point[1], working_point[0]))
            lines.append(r)
    return lines
