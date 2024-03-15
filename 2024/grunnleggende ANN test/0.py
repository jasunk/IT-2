import matplotlib.pyplot as plt
import numpy as np
import random

#x = np.array([0,9])
#y = np.array([0,9])

feilVekt = [11,14,15, 12, 13, 15, 16]
feilRad  = [6,6,7,8,7,9,8]
rettVekt = [9,8,6,7,9,8,7]
rettRad  = [4,5,3,2,4,4,5]

feil_w = 13
rett_w = 17

test_x = 14
test_y =  8

bias = 10

xline=np.array([0, rett_w])
yline=np.array([feil_w, 0])

plt.scatter(feilVekt,feilRad, color="pink")
plt.scatter(rettVekt,rettRad, color="blue")
plt.scatter(test_x,test_y, color="red")

plt.plot(xline, yline,color = "green")
plt.show()