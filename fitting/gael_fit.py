import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

data2plot = pd.read_csv('data.csv', delimiter=',', engine='python')

x_line = data2plot['Temps[min]'].to_numpy()
y_line = data2plot['Température'].to_numpy()

z = np.polyfit(x_line, y_line, deg=7)
p = np.polyval(z, x_line)  # polyfit
print(f'max: {round(max(p),2)}')

data2plot['Temps-polyfit'] = pd.Series(p)  # to include the polyfit in the dataframe

print(data2plot.tail())

sns.lineplot(y='Température', x='Temps[min]', data=data2plot, color='blue')
graph = sns.lineplot(y='Temps-polyfit', x='Temps[min]', data=data2plot, color='orange')
graph.annotate(f'max: {round(max(p),2)}', xy=(450, 605))
plt.legend(labels=['Ideal Temperature', 'Fit Temperature'])
plt.show()