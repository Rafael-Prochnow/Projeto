import pandas as pd
import os

path = r'C:\Users\Elen- PC\Jupyter\teste'
files = os.listdir(path)
df = pd.DataFrame()

print(files)

files_csv = [path + '\\' + f for f in files if f[-3:] == 'csv']
print(files_csv)

for f in files_csv:
    data = pd.read_csv(f)
    df = df.append(data)

print(df)
