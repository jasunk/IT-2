import numpy as np
import math
w_1 = [1]
x_1 = [1]
b_1 = 1

def samlet(w,x,b):
    return sum(x[i] * w[i] for i in range(0, len(x)))+b

def boolean_node(x):
    if x>=0:
        return 1
    return 0

def sigmoid_node(x):
    return (1)/(1+math.e**-x)

print(boolean_node(samlet(w_1, x_1, b_1)))
print(sigmoid_node(samlet(w_1, x_1, b_1)))