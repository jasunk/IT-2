import matplotlib.pyplot as plt

def animer_nozoom(array1, array2, fart=0.1):
    plt.xlim(array1[0], array1[-1])
    plt.ylim(array2[0], array2[-1])
    for i in range(len(array1)):
        plt.plot(array1[:i], array2[:i], 'ro-')
        plt.pause(fart)

def animer_zoom(array1, array2, fart=0.1):

    for i in range(len(array1)):
        plt.plot(array1[:i], array2[:i], 'ro-')
        plt.pause(fart)


