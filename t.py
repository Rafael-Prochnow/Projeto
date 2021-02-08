import pandas as pd


dados = pd.read_csv("Tabela_geral_2019_nova.csv")
UNIFACISA = dados.query("Time == 'UNIFACISA'").reset_index(drop=True)

data = {'Total Cpu Time': ['00:00:14', '00:00:15', '00:00:16', '00:00:17'], 'Date': ['2019-02-07', '2019-02-07', '2019-02-08', '2019-02-08'] }

df = pd.DataFrame(data, columns=['Total Cpu Time', 'Date'])
print(type(df['Total Cpu Time'][0]))

df['Date'] = pd.to_datetime(df['Date'])
df['Total Cpu Time'] = pd.to_timedelta(df['Total Cpu Time'])
print(df)

'''



print(df)

grouped = df['Total Cpu Time'].groupby(df['Date']).sum()
print(grouped)

'''