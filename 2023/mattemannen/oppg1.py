
måneder={
    "januar":1,
    "februar":2,
    "mars":3,
    "april":4,
    "mai":5,
    "juni":6,
    "juli":7,
    "august":8,
    "september":9,
    "oktober":10,
    "november":11,
    "desember":12

}
def T(x):
    if 2<=x<=10:
        return (0.048*x**4-1.4*x**3+13.36*x**2-45.8*x+35.2)
    pass


h = 0.00000000000001
def derivertT(x):

    return((T((x+h))-T(x))/h)


def antOverNull(start,slutt):

    try:
        start, slutt = måneder[start], måneder[slutt]
    except ValueError:
        print("wallah")

    overNull = []
    for i in range(int(start),int(slutt)+1):
        if T(i) > 0:
            overNull.append(i)

    return (len(overNull)*30)

print(f"Ca {antOverNull('februar', 'oktober')} dager var temp over 0 ")


for x in range(2,10):
    print(derivertT(x))
