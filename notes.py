import collections
from collections import Counter
from scipy.ndimage import gaussian_filter
import numpy as np

def plus_minus():
    value = np.random.random(1)[0]
    if value>0.5:
        return 1
    return -1
print(plus_minus())
# test_list_x = collections.deque([2.97, 2.97, 3, 2.67, 2.67])
# deq_mean = np.mean(test_list_x)
# deq_var = np.var(test_list_x)
# deq_std = np.std(test_list_x)
# next_number = 2.8
# print(np.var(test_list_x))
# print(np.std(test_list_x))
# print(np.mean(test_list_x))
# print(test_list_x[0])
# if (deq_mean-deq_std) < (next_number) < (deq_mean+deq_std):
#     test_list_x.appendleft(next_number)
#     print(f"yay new deq is > {test_list_x}")
# else:
#     print(f"noo the num is too huge>> {next_number}")
# print(np.std(test_list_x))
