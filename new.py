import pretty_errors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pretty_errors.activate()

import matplotlib.pyplot as plt
# Read data from CSV file
data = pd.read_table('sources/boston_house_prices.csv')

df = pd.DataFrame(data=np.random.randint(1,13,size=(10,14)),
                  columns=['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV'])
# Plot the data
df[['CRIM','ZN']].plot(kind='line', marker='o')
# Read the 'CRIM' and 'ZN' columns from the data
x = df['CRIM']
y = df['ZN']

# Plot the data
plt.plot(x, y, marker='o')
plt.title('Line Plot')
plt.grid(True)
plt.show()