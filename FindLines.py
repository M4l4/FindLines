import numpy as np


def trace_line(img, shape, centre, result=None, start=True, last=None) -> "Tuple array":
    """ Recursively traces a line in a binary array, returning the endpoints.

    :param img: Binary image as a NumPy array with one pixel wide lines.
    :param shape: np.shape(img) Passed as an argument to save function calls.
    :param centre: The location in the image.
    :param result: Array to append the points as they are found.
    :param start: If this is the first call of the function, or a recursion.
    :param last: Which direction the line is being traced.
    :return: Returns an array of two tuples, the two end points of the line, or nothing.
    """

    if start:
        result = []

    # If we have more than two endpoints found so far, exit. Who knows what happened.

    if len(result) > 2:
        return

    line_adjacent = []
    direction2 = 0

    left, right, top, bottom = False, False, False, False
    if centre[0] == 0:
        top = True
    if centre[0] == shape[0]-1:
        bottom = True
    if centre[1] == 0:
        left = True
    if centre[1] == shape[1] - 1:
        right = True

    # The 8 pixels around the center point are given numbers as
    # follows:
    # 1 8 7
    # 2 x 6
    # 3 4 5

    if not left:
        if not top:
            if img[centre[0]-1, centre[1]-1]:
                line_adjacent.append(1)
        if img[centre[0], centre[1]-1]:
            line_adjacent.append(2)
        if not bottom:
            if img[centre[0]+1, centre[1]-1]:
                line_adjacent.append(3)
    if not bottom:
        if img[centre[0]+1, centre[1]]:
            line_adjacent.append(4)
    if not right:
        if not bottom:
            if img[centre[0]+1, centre[1]+1]:
                line_adjacent.append(5)
        if img[centre[0], centre[1]+1]:
            line_adjacent.append(6)
        if not top:
            if img[centre[0]-1, centre[1]+1]:
                line_adjacent.append(7)
    if not top:
        if img[centre[0]-1, centre[1]]:
            line_adjacent.append(8)

    # If the centre point is an endpoint, either find the other end if this is the first iteration or return otherwise.

    if len(line_adjacent) == 1:
        result.append(centre)
        if start:
            direction = line_adjacent[0]
        else:
            return result

    # If the centre point is a midpoint, either recurse down both sides if this is the first iteration or only down the
    # side that is in the same direction that was moved last time.  If neither of the options satisfy that, exit.
    # `last` is an array indicating the direction to travel down the line.  This serves to limit the lines that can be
    # followed to a single direction, so that it doesn't end up going in literal circles.

    elif len(line_adjacent) == 2:
        if not start:
            if line_adjacent[0] in last:
                direction = line_adjacent[0]
            elif line_adjacent[1] in last:
                direction = line_adjacent[1]
            else:
                return
        else:
            direction = line_adjacent[0]
            direction2 = line_adjacent[1]

    # If there are zero or more than two adjacent points, exit.

    else:
        return

    if start:
        last = [direction - 1, direction, direction + 1]
        if last[0] == 0:
            last[0] = 8
        if last[2] == 9:
            last[2] = 1

    n_centre = new_centre(centre, direction)
    trace_line(img, shape, n_centre, result, False, last)

    # If the starting point was a midpoint, recurse down the other branch.
    if start:
        last = [direction2 - 1, direction2, direction2 + 1]
        if last[0] == 0:
            last[0] = 8
        if last[2] == 9:
            last[2] = 1

    if direction2:
        n_centre = new_centre(centre, direction2)
        trace_line(img, shape, n_centre, result, False, last)

    # If we have more or less than two endpoints by now, something went wrong.

    if len(result) == 2:
        return result
    else:
        return


def new_centre(old_centre, direction):
    if direction == 1:
        return old_centre[0]-1, old_centre[1]-1
    elif direction == 2:
        return old_centre[0], old_centre[1]-1
    elif direction == 3:
        return old_centre[0]+1, old_centre[1]-1
    elif direction == 4:
        return old_centre[0]+1, old_centre[1]
    elif direction == 5:
        return old_centre[0]+1, old_centre[1]+1
    elif direction == 6:
        return old_centre[0], old_centre[1]+1
    elif direction == 7:
        return old_centre[0]-1, old_centre[1]+1
    elif direction == 8:
        return old_centre[0]-1, old_centre[1]


def find_lines(img) -> "Tuple array":
    """Finds and returns the end point of lines on a binary image.

    Returns only lines that are at least two pixels long and do not intersect any other lines.

    :param img: Binary image as a NumPy array with one pixel wide lines.
    :return: List of line end point tuples in the form of ((p0.x, p0.y), (p1.x, p1,y))
    """

    lines = []
    for rr in range(0, np.shape(img)[0]):
        for cc in range(0, np.shape(img)[1]):
            if img[rr, cc]:
                points = trace_line(img, np.shape(img), (rr, cc))
                if points:
                    lines.append(tuple(points))

    final_lines = set()
    for i in lines:
        if not (i in final_lines or tuple([i[1], i[0]]) in final_lines):
            final_lines.add(i)

    return final_lines
