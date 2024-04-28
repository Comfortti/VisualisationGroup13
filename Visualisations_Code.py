import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
#
#Retrieve data
df = pd.read_csv('demanddata2009_2024.csv')
#
# Pre-processing
# 1) remove columns with Null values
# Identify columns with null values and set to zero
dfna=df.columns[df.isna().any()].tolist()
df[dfna] = df[dfna].fillna(0)
#check result
#print(df.isna().any())
#
# 2) Drop rows if settlement_period value is greater than 48
df.drop(index=df[df["SETTLEMENT_PERIOD"] > 48].index, inplace=True)
df.reset_index(drop=True, inplace=True)
#
# 3) Transform Settlement date into date/time, format: yyyy-mm-dd hh:mm:ss
# Lambda function used to turn settlement period into hours.
# Settlement period equal to 0 corresponds with 00:00:00 and 48 with 23:30:00
df['PERIOD_HOUR'] = (df['SETTLEMENT_PERIOD']).apply(lambda x: str(dt.timedelta(hours=(x - 1) * 0.5)))
df.loc[df['PERIOD_HOUR'] == '1 day, 0:00:00', 'PERIOD_HOUR'] = '0:00:00'
df['SETTLEMENT_DATE'] = df['SETTLEMENT_DATE'].apply(lambda x: str(dt.datetime.strptime(x, '%Y-%m-%d').strftime('%Y/%m/%d')))
df['SETTLEMENT_DATE'] = pd.to_datetime((df['SETTLEMENT_DATE'] + ' ' + df['PERIOD_HOUR']))
#
# 4) Categorization for visualizations
df['YEAR'] = df['SETTLEMENT_DATE'].dt.year
seasons = {1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring', 6: 'Summer', 7: 'Summer', 8: 'Summer', 9: 'Autumn', 10: 'Autumn', 11: 'Autumn', 12: 'Winter'}
df['SEASON'] = df['SETTLEMENT_DATE'].dt.month.map(seasons)
df['SEASON_YEAR'] = np.where(df['SETTLEMENT_DATE'].dt.month == 12, df['YEAR'] + 1, df['YEAR'])
cols = ['SEASON_YEAR', 'SEASON']
df['YEAR_SEASON'] = df[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
df['HOUR'] = df['SETTLEMENT_DATE'].dt.hour
#
# 5) Reset index
df.set_index('SETTLEMENT_DATE', inplace=True)
#
# Test values created correctly
#print(df.head)
##selected_rows = df.query('YEAR == 2021')
##print(selected_rows.head) # checks SEASON_YEAR
#
# Charts
# 1) Stacked chart of annual total embedded Solar on embedded Wind energy capacity in Terawatts
#group and divide values by 1,000,000 (values now in Terawatts)
A = np.array(df.YEAR.unique())
B = np.array(df.groupby('YEAR').sum().eval('EMBEDDED_WIND_CAPACITY / 1000000'))
C = np.array(df.groupby('YEAR').sum().eval('EMBEDDED_SOLAR_CAPACITY / 1000000'))
#drop last column (2024 as incomplete year)
A = A[:-1]
B = B[:-1]
C = C[:-1]
#Check values to be displayed
#print('\n',A)
#print('\n',B)
#print('\n',C)
#print('\n',len(A))
#build graph
x = np.arange(len(A)) # the x locations for the groups
p1 = plt.bar(x, B)
p2 = plt.bar(x, C, bottom=B)
plt.legend((p1[0], p2[0]), ('Wind', 'Solar'))
plt.xticks(x, A)
plt.xlabel('Year')
plt.ylabel('Total annual embedded capacity (Terawatts)')
plt.title('Embedded Wind and Solar capacity')
plt.show()
#
# 2) Group bar chart of total embedded Wind energy generated in Terawatts over each season over last 4 years
#group season totals and divide by 1,000,000 (values now in Terawatts)
A = np.array(df.SEASON_YEAR.unique())
B = np.array(df.groupby('YEAR_SEASON').sum().eval('EMBEDDED_WIND_GENERATION / 1000000'))
#drop years preceding 2020 and incomplete 2024
A = A[11:-1] #years
B = B[44:-2]
#build graph
sb.set()
sb.set_style("ticks")
column_names = ['Winter', 'Spring', 'Summer', 'Autumn']
C = pd.DataFrame(B.reshape(4,4),index=A,columns=column_names)
colours=('black','blue','yellow','orange')
C.plot.bar(legend=True, width=0.8, figsize=(2,5),title='Total embedded wind power generated per season over last 4 years',xlabel='Seasons per year',ylabel='Total embedded wind power generated\nper season (Terawatts)',color=colours)
plt.show()
#
# 3) Heat map of annual total for each hour of embedded Solar energy generated in Terawatts since 2009 
#A = df.groupby(['YEAR','HOUR'])['EMBEDDED_SOLAR_GENERATION'].sum()
A = df.groupby(['YEAR','HOUR']).sum().eval('EMBEDDED_SOLAR_GENERATION / 1000000')
A = A.reset_index(name='SOLAR_GEN_HR')
A = sb.heatmap(A.pivot(index='YEAR',columns='HOUR',values='SOLAR_GEN_HR'),cmap='magma',cbar_kws={'label': 'Terawatts'})
A.invert_yaxis()
plt.title('Total embedded solar power generated per hour per year')
plt.show()
#
# 4) a) Wind utilization
A = np.array(df.YEAR.unique())
A = A[:-1] #years, removing incomplete 2024
#grouped values and divided by 1,000,000 (values now in Terawatts)
B = np.array(df.groupby('YEAR').sum().eval('EMBEDDED_WIND_CAPACITY / 1000000'))
B = B[:-1] #wind capacity, removing incomplete 2024
C = np.array(df.groupby('YEAR').sum().eval('EMBEDDED_WIND_GENERATION / 1000000'))
C = C[:-1] #wind generation, removing incomplete 2024
#Check values to be displayed
#print('\n',A)
#print('\n',B)
#print('\n',C)
plt.plot(A,B,color='blue',linestyle = 'dashed',label='Estimated embedded\nWind Capacity')
plt.plot(A,C,color='orange',linestyle = 'dashed',label='Estimated embedded Wind\nEnergy Generated')
plt.fill_between(A, B, C, color='green', alpha=0.2,label='Unutilised embedded\nwind energy capacity')
plt.title('Estimated embedded Wind energy utilisation')
plt.ylabel('Total annual estimated embedded\nwind power (Terawatts)')
plt.ylim(0,120)
plt.xlabel('Year')
plt.legend(loc='upper left', title='Legend')
plt.show()
#
# 4) b) Solar utilization
A = np.array(df.YEAR.unique())
A = A[:-1] #years, removing incomplete 2024
#grouped values and divided by 1,000,000 (values now in Terawatts)
B = np.array(df.groupby('YEAR').sum().eval('EMBEDDED_SOLAR_CAPACITY / 1000000'))
B = B[:-1] #Solar capacity, removing incomplete 2024
C = np.array(df.groupby('YEAR').sum().eval('EMBEDDED_SOLAR_GENERATION / 1000000'))
C = C[:-1] #Solar generation, removing incomplete 2024
#Check values to be displayed
#print('\n',A)
#print('\n',B)
#print('\n',C)
plt.plot(A,B,color='blue',linestyle = 'dashed',label='Estimated embedded\nSolar Capacity')
plt.plot(A,C,color='red',linestyle = 'dashed',label='Estimated embedded Solar\nEnergy Generated')
plt.fill_between(A, B, C, color='yellow', alpha=0.2,label='Unutilised estimated embedded\nsolar energy capacity')
plt.title('Estimated embedded Solar energy utilisation')
plt.ylabel('Total annual estimated embedded\nsolar power (Terawatts)')
plt.ylim(0,300)
plt.xlabel('Year')
plt.legend(loc='upper left', title='Legend')
plt.show()
