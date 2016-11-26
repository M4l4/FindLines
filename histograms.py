import matplotlib
matplotlib.use("TkAgg")     # Fixes error on OSX
import numpy as np
import math
import matplotlib.pyplot as plt
import os
import re
from pathlib import Path
import scipy.stats as stats

folder = "D:\\res"
files = []

for f in os.listdir(folder):
    if re.search('(?i).*error-.*\.npy', f):
        files.append(str(Path(folder + "\\" + f).resolve()))
        # print(str(f))

for f in files:
    path = Path(f)
    hough = np.load(f)

    hough_heading = []
    hough_length = []
    for x, l in enumerate(hough):
        p0, p1 = l
        heading = math.degrees(math.atan2((p1[1] - p0[1]), (p1[0] - p0[0])))
        # if not (heading == 0 or abs(heading) == 45):
        hough_heading.append(heading)

    # with open("D:\\headings\\" + path.stem + "no-0.txt", 'w') as l:
    #     for x, h in enumerate(hough_heading):
    #         l.write(str(h) + '\n')

    hough_hist, edges = np.histogram(hough_heading, 90, (-90, 90))
    # with open("D:\\hist\\" + path.stem + "bins.txt", 'w') as l:
    #     for x, h in enumerate(hough_hist):
    #         l.write(str((x-18)*5) + ', ' + str((x-18)*5+5) + ': ' + str(h) + '\n')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.suptitle(path.stem)
    ax.set_title(stats.kstest(hough_heading, 'norm'))
    for x, h in enumerate(hough_hist):
        ax.text((x-45)*2, 50, str(h), ha='center', va='top', rotation=60)
    ax.xaxis.set_ticklabels([])
    plt.bar(edges[:-1], hough_hist, width=2)
    # for rect in rects:
    #     height = rect.get_height()
    #     ax.text(rect.get_x() + rect.get_width()/2., 1.05*height, '%d' % int(height), ha='center', va='bottom')
    plt.xlim(min(edges), max(edges))
    plt.ylim(0, 12000)
    # plt.show()
    plt.savefig("D:\\hist\\" + path.stem + "_90.pdf", format='pdf')
    plt.close()
    # print('done: ' + path.stem)
