import numpy as np
import math
from skimage.draw import line
import matplotlib.pyplot as plt


def find_distance(point1, point2):
    return math.sqrt(math.pow((point1[1]-point2[1]), 2)+math.pow((point1[0]-point2[0]), 2))


def min_dist(l1, l2):
    dist = find_distance(l1[0], l2[0])
    x = 0
    if find_distance(l1[1], l2[0]) < dist:
        x = 1
    if find_distance(l1[1], l2[1]) < dist:
        x = 2
    if find_distance(l1[0], l2[1]) < dist:
        x = 3

    if x == 3:
        ret = [l1[0], l2[1], l1[1], l2[0]]
    elif x == 2:
        ret = [l1[1], l2[1], l1[0], l2[0]]
    elif x == 1:
        ret = [l1[1], l2[0], l1[0], l2[1]]
    else:
        ret = [l1[0], l2[0], l1[1], l2[1]]

    return ret

long_long = []

result_lines = np.load('D:\\15201_769_error_result-lines.npy')

result_heading = [[x] for x in range(90)]

for l in result_lines:
    p0, p1 = l
    result_heading[round((int(math.degrees(math.atan2((p1[1] - p0[1]), (p1[0] - p0[0])))) + 90) / 2)].append(tuple([p0, p1]))

for i in result_heading:
    i.pop(0)

for x in range(len(result_heading)):
    for a in range(len(result_heading[x])):
        i = result_heading[x].pop()
        if not x == len(result_heading) - 1:
            ll = result_heading[x]  # + result_heading[x-1] + result_heading[x+1]
        else:
            ll = result_heading[x]  # + result_heading[x-1] + result_heading[0]
        for b in ll:
            close1, close2, long1, long2 = min_dist(i, b)
            if math.fabs(((math.degrees(math.atan2((close2[1] - close1[1]), (close2[0] - close1[0])))+90) / 2) - x) < 1:
                if find_distance(long1, long2) < 1000:
                    long_long.append((long1, long2))

plot = np.zeros((3270, 5003))
for x in long_long:
    p0, p1 = x
    rr, cc = line(int(p0[1]), int(p0[0]), int(p1[1]), int(p1[0]))
    plot[rr, cc] = True
plt.imsave("D:\\long_long.pdf", plot, cmap='Greys')
plot2 = np.zeros((3270, 5003))
