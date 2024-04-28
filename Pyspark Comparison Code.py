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
#Python
#start processing
start = dt.datetime.now()
A = np.array(df.YEAR.unique())
B = np.array(df.groupby('YEAR')['EMBEDDED_WIND_CAPACITY'].sum())
C = np.array(df.groupby('YEAR')['EMBEDDED_SOLAR_CAPACITY'].sum())
#drop last column (2024 as incomplete year)
A = A[:-1]
B = B[:-1]
C = C[:-1]
#divide values by 1,000,000 (values now in Terawatts)
x = 1000000 
B = np.divide(B,x)
C = np.divide(C,x)
end = dt.datetime.now()
print('\npython section')
print('\nstart time: ',start,'\n  end time: ',end, '\nduration: ',end-start,'\n')
#Check values
#print('\n',A)
#print('\n',B)
#print('\n',C)
#
#Spark set up
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import findspark
findspark.init()
###spark (g4g) https://www.geeksforgeeks.org/how-to-convert-pandas-to-pyspark-dataframe/
# Building the SparkSession and name it :'pandas to spark'
spark = SparkSession.builder.appName("pandas to spark").getOrCreate()
# enabling the Apache Arrow for converting Pandas df to pySpark DF(DataFrame)
spark.conf.set("spark.sql.execution.arrow.enabled", "true")
# Creating the DataFrame
sdf = spark.createDataFrame(df)
#
#Spark
#start processing
start = dt.datetime.now()
X=sdf.select('YEAR').distinct()
Y=sdf.groupBy('YEAR').agg({'EMBEDDED_WIND_CAPACITY': 'sum'})
Z=sdf.groupBy('YEAR').agg({'EMBEDDED_SOLAR_CAPACITY': 'sum'})
#drop last column (2024 as incomplete year)
X=X.where(X.YEAR != '2024')
Y=Y.where(Y.YEAR != '2024')
Z=Z.where(Z.YEAR != '2024')
Y=Y.withColumn('sum(EMBEDDED_WIND_CAPACITY)',col('sum(EMBEDDED_WIND_CAPACITY)') / 1000000)
Z=Z.withColumn('sum(EMBEDDED_SOLAR_CAPACITY)',col('sum(EMBEDDED_SOLAR_CAPACITY)') / 1000000)
end = dt.datetime.now()
print('spark section')
print('\nstart time: ',start,'\n  end time: ',end, '\nduration: ',end-start,'\n')
#Check values
#X.show()
#Y.show()
#Z.show()