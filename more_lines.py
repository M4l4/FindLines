import numpy as np
import math


def find_distance(p1, p0):
    return math.sqrt(math.pow((p1[1]-p0[1]), 2)+math.pow((p1[0]-p0[0]), 2))

long_result_lines = np.load('D:\\saved-split\\twice_15205_379_error_result-lines.npy')
print(long_result_lines.size)

result_heading = [[x] for x in range(90)]
print(result_heading)
for l in long_result_lines:
    p0, p1 = l
    result_heading[math.floor((int(math.degrees(math.atan2((p1[1] - p0[1]), (p1[0] - p0[0])))) + 90) / 2)].append(tuple([p0, p1]))

for i in result_heading:
    i.pop(0)

for x, i in enumerate(result_heading):
    x = 1
    l_list = result_heading[x] + result_heading[x-1] + result_heading[x+1]
    for a in l_list:
        for b in l_list:
            min_d = (a[0], b[0])
            if find_distance(a[0], b[1]) < find_distance(min_d[0], min_d[1]):
                min_d = (a[0], b[1])
            if find_distance(a[1], b[0]) < find_distance(min_d[0], min_d[1]):
                min_d = (a[1], b[0])
            if find_distance(a[1], b[1]) < find_distance(min_d[0], min_d[1]):
                min_d = (a[1], b[1])
            compare = math.degrees(math.atan2((min_d[1][1] - min_d[0][1]), (min_d[1][0] - min_d[0][0])))

    print('')
