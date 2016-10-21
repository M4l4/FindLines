import numpy as np
from scipy.ndimage.filters import convolve
from collections import deque


def find_lines(img):
    print('finding.........')
    lines = []
    w = [[1, 1, 1],
         [1, 10, 1],
         [1, 1, 1]]
    b = convolve(img.astype(int), w)
    b *= (b > 10)
    l = deque(np.argwhere(b == 11))
    while l:
        x = l.pop()
        if b[x[0], x[1]] != 11:
            continue
        n = x
        t = True
        while t:
            b[n[0], n[1]] = 0
            c = (b[n[0] - 1:n[0] + 2, n[1] - 1:n[1] + 2])
            p = np.flatnonzero(c)
            if p:
                p = p[0]
            else:
                break
            if p == 0:
                n = (n[0] - 1, n[1] - 1)
            elif p == 1:
                n = (n[0] - 1, n[1])
            elif p == 2:
                n = (n[0] - 1, n[1] + 1)
            elif p == 3:
                n = (n[0], n[1] - 1)
            elif p == 5:
                n = (n[0], n[1] + 1)
            elif p == 6:
                n = (n[0] + 1, n[1] - 1)
            elif p == 7:
                n = (n[0] + 1, n[1])
            elif p == 8:
                n = (n[0] + 1, n[1] + 1)
            if b[n[0], n[1]] == 11:
                b[n[0], n[1]] = 0
                t = False
                continue
            if (b[n[0], n[1]]) != 12:
                break
        else:
            r = ((x[1], x[0]), (n[1], n[0]))
            lines.append(r)
    return lines
