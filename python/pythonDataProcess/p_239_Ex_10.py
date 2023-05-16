import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'

filename = 'mpg.csv'
myframe = pd.read_csv(filename, encoding='utf-8', index_col=0)

print(myframe['jumsu'].unique())