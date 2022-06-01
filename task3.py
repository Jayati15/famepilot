import numpy as np

def find_roots(a, b, c):
    input = [a, b, c]
    return tuple(np.roots(input))

print(find_roots(2, 10, 8));