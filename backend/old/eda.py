import pandas as pd

df = pd.read_csv('ipip/data-final.csv')

df = df['Country']

print(df.head())
