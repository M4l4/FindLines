import numpy as np
from skimage.transform import probabilistic_hough_line


def hough_split(img, splits, shape, overlap):
    temp = []
    cc_edges = np.repeat(np.linspace(shape[1]/splits, shape[1], splits-1, False, dtype=int), 2)
    rr_edges = np.repeat(np.linspace(shape[0]/splits, shape[0], splits-1, False, dtype=int), 2)
    print(shape)
    print("(" + str(shape[0]/splits) + ", " + str(shape[1]/splits) + ")")
    cc_edges[::2] += overlap
    cc_edges[1::2] -= overlap
    rr_edges[::2] += overlap
    rr_edges[1::2] -= overlap
    cc_edges = np.concatenate(([0], cc_edges, [shape[1]]))
    rr_edges = np.concatenate(([0], rr_edges, [shape[0]]))

    for i in range(0, splits*2, 2):
        for j in range(0, splits*2, 2):
            slice_t = img[rr_edges[i]:rr_edges[i+1], cc_edges[j]:cc_edges[j+1]]
            array = np.asarray(probabilistic_hough_line(slice_t, 40, 0)[:])
            if array.size:
                array[:, :, ::2] += cc_edges[j]
                array[:, :, 1::2] += rr_edges[i]

            temp.append(array)

    res = np.array(temp[0])
    for i in range(1, len(temp)):
        res = np.append(res, temp[i])
    res = np.reshape(res, (-1, 2, 2))

    return res
