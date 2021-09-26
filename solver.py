import numpy as np
from math import inf


def permutations(pos, n, k):
    base_list = [item for item in range(pos, n)]
    if k == 1:
        return base_list
    result = []
    for element in base_list:
        append_list = permutations(element + 1, n, k - 1)
        for append_num in append_list:
            if isinstance(append_num, int):
                append_num = [append_num]
            extend_list = [element]
            extend_list.extend(append_num)
            result.append(extend_list)
    return result


# noinspection PyBroadException
def solver(basic_arr, b, f):
    columns_to_0 = permutations(0, len(basic_arr[0]), len(basic_arr[0]) - len(b))
    results = []
    for permutation in columns_to_0:
        temp_arr = basic_arr
        counter = 0
        for i in permutation:
            temp_arr = np.delete(temp_arr, i - counter, 1)
            counter += 1
        try:
            solution = np.linalg.solve(temp_arr, b)
            if not any(x < 0 for x in solution):
                results.append([permutation, solution])
        except:
            pass

    result_points = []
    for result in results:
        result_point = []
        counter = 0
        for i in range(len(basic_arr[0])):
            if counter < len(result[0]) and i == result[0][counter]:
                result_point.append(0)
                counter += 1
            else:
                result_point.append(result[1][i - counter])
        result_points.append(result_point)

    max_result = -inf
    max_point = []
    for point in result_points:
        if f(point) > max_result:
            max_point = point
            max_result = f(point)

    return max_result, max_point


if __name__ == "__main__":
    arr = np.array(
        [[0.0, 1.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0],
         [0.0, 1.8, 1.8, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
         [1.6, 0.0, 0.0, 1.2, 0.0, 0.0, 1.0, 0.0, 0.0],
         [5.0, 6.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
         [0.0, 0.0, 4.0, 4.0, 0.0, 0.0, 0.0, 0.0, 1.0]])

    restrictions = np.array(
        [10.0,
         36.0,
         20.0,
         80.0,
         80.0])

    #print(solver(arr, restrictions, lambda x: 10 * x[0] + 15 * x[1] + 15 * x[2] + 18 * x[3]))
    print((permutations(0, 4, 2)))
