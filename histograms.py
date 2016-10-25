import matplotlib
matplotlib.use("TkAgg")     # Fixes error on OSX
import numpy as np
import math
import matplotlib.pyplot as plt

hough = np.load("C:\\Malachite\\saved-split\\twice_15205_379_error_error-lines.npy")
# result = np.load("/Users/mal/FindLines/saved-split/long_15205_380_no_result-lines.npy")

hough_heading = []
hough_length = []
for x, l in enumerate(hough):
        p0, p1 = l
        hough_heading.append(math.degrees(math.atan2((p0[0] - p1[0]), (p0[1] - p1[1]))))


# res_heading = []
# res_length = []
# for l in result:
#     p0, p1 = l
#     res_heading.append(math.degrees(math.atan2((p0[0] - p1[0]), (p0[1] - p1[1]))))
#     res_length(math.sqrt(math.pow((p1[1] - p0[1]), 2) + math.pow((p1[0] - p0[0]), 2)))

hough_hist, edges = np.histogram(hough_heading, 180, (-90, 90))
# res_hist, _ = np.histogram(res_heading, 180, (-90, 90))
#
# diff_hist = hough_hist - res_hist
#
plt.bar(edges[:-1], hough_hist, width=1)
plt.xlim(min(edges), max(edges))
# plt.savefig("C:\\Malachite\\figs\\bcd15202_651-hough.pdf", format='pdf')
plt.show()
