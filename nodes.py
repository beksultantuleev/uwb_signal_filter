import collections
from collections import Counter
from scipy.ndimage import gaussian_filter

def my_mode(sample):
    c = Counter(sample)
    return [k for k, v in c.items() if v == c.most_common(1)[0][1]]

my_deque = collections.deque([])
my_deque.appendleft(1)#oldest
my_deque.appendleft(2)
my_deque.appendleft(3)
my_deque.appendleft(3)
gaus_deque = gaussian_filter(my_deque, 4)
# print(f"original> {my_deque} \n gaus deque > {gaus_deque}")
# print(my_deque.pop())
print(my_mode(my_deque))