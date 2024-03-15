frukter = ["eple", "pære", "appelsin", "mango", "kiwi", "nåkke søtt"]
smak = ["surt om det er grønt, søtt om det er rødt", "søtt", "surt", "søtt", "surt", "søtt"]

while True:
    inp = input("Skriv inn en frukt:  ").lower()

    if inp in frukter:
        print(f"{inp} smaker {smak[(frukter.index(inp))]}")
    else:
        print(f"{inp} er ikke i listen, prøv en annen frukt :)")
