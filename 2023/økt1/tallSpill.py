import random as r

inpTall = float(input("Prøv å gjette tallet mellom 0 og 10: "))
tilfTall = r.randint(0,10)

if inpTall<tilfTall:
    print(f"Du gjettet for lavt man, tallet var {tilfTall}")
elif inpTall>tilfTall:
    print(f"Du gjettet for høyt man, tallet var {tilfTall}")
elif inpTall==tilfTall:
    print(f"NO WAY HOMIE, DU GJETTET RETT! Tallet var {tilfTall}")