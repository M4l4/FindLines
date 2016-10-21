import numpy as np
from skimage.transform import probabilistic_hough_line


def hough_split(img, splits, shape, path):
    temp = []
    cc_edges = np.repeat(np.linspace(shape[1]/splits, shape[1], splits-1, False, dtype=int), 2)
    rr_edges = np.repeat(np.linspace(shape[0]/splits, shape[0], splits-1, False, dtype=int), 2)
    # cc_edges[::2] += 15
    # cc_edges[1::2] -= 15
    # rr_edges[::2] += 15
    # rr_edges[1::2] -= 15
    cc_edges = np.concatenate(([0], cc_edges, [shape[1]]))
    rr_edges = np.concatenate(([0], rr_edges, [shape[0]]))
    # print(cc_edges)
    # print(rr_edges)
    # print('----------')
    # print(img.shape)

    # print(cc_edges.shape[0], rr_edges.shape[0])
    for i in range(0, splits*2, 2):
        for j in range(0, splits*2, 2):
            slice_t = img[rr_edges[i]:rr_edges[i+1], cc_edges[j]:cc_edges[j+1]]
            array = np.asarray(probabilistic_hough_line(slice_t, 10, 30)[:])
            if array.size:
                array[:, :, ::2] += cc_edges[j]
                array[:, :, 1::2] += rr_edges[i]

            temp.append(array)

    # temp = np.array(temp).reshape(50, 50)
    # for i in range(0, splits*2, 2):
    #     for j in range(0, splits*2, 2):
    #         if temp[int(i/2), int(j/2)].size:
    #             temp[int(i/2), int(j/2)][:, :, 0] += rr_edges[i]
    #             temp[int(i/2), int(j/2)][:, :, 1] += cc_edges[j]
    # temp = temp.flatten()
    res = np.array(temp[0])
    for i in range(1, len(temp)):
        res = np.append(res, temp[i])
    res = np.reshape(res, (-1, 2, 2))
    # print(res)
    # np.save("C:\\Malachite\\saved\\line_report_" + path.stem + "_new-lines.npy", np.array(res))

    return res
