import matplotlib
matplotlib.use("TkAgg")     # Fixes error on OSX
import numpy as np
import math
import matplotlib.pyplot as plt

hough = np.load("C:\\Malachite\\saved-split\\twice_15201_769_error_error-lines.npy")

hough_heading = []
hough_length = []
for x, l in enumerate(hough):
        p0, p1 = l
        # hough_heading.append(math.degrees(math.atan2((p0[0] - p1[0]), (p0[1] - p1[1])))) # HOUGH
        hough_heading.append(math.degrees(math.atan2((p1[1] - p0[1]), (p1[0] - p0[0])))) # FOUND

hough_hist, edges = np.histogram(hough_heading, 45, (-90, 90))

plt.bar(edges[:-1], hough_hist, width=4)
plt.xlim(min(edges), max(edges))
# plt.savefig("C:\\Malachite\\figs\\bcd15202_651-hough.pdf", format='pdf')
plt.show()
