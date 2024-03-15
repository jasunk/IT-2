import pandas as pd

import matplotlib.pyplot as plt

#åpner og leser "month" og "nightly rate" fra filen "market_analysis.csv" og ignorerer feilmeldinger
data = pd.read_csv("market_analysis.csv", on_bad_lines="warn", sep=";")


month = [int(d) for d in data['revenue']]

nightly_rate = list(data['nightly rate'])
print(month)
plt.plot(month, nightly_rate)
plt.show()

