import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("demanddata2009_2024_A.csv")

# Convert the "SETTLEMENT_DATETIME" column to datetime format
df['SETTLEMENT_DATETIME'] = pd.to_datetime(df['SETTLEMENT_DATETIME'])

# Set the "SETTLEMENT_DATETIME" column as the index
df.set_index('SETTLEMENT_DATETIME', inplace=True)

# Take absolute values of the columns
df_abs = df.abs()

# Resample the data on a monthly basis and calculate the sum for each month
df_monthly_sum = df_abs.resample('ME').sum()

# Plot the time series for National Demand
plt.figure(figsize=(10, 6))
plt.plot(df_monthly_sum.index, df_monthly_sum['ND'], color='blue', linestyle='-', label='Total National Demand')

# Plot the time series for Transmission System Demand
plt.plot(df_monthly_sum.index, df_monthly_sum['TSD'], color='green', linestyle='-', label='Total Transmission System Demand')

# Plot the time series for England Wales Demand
plt.plot(df_monthly_sum.index, df_monthly_sum['ENGLAND_WALES_DEMAND'], color='red', linestyle='-', label='Total England Wales Demand')

plt.title('Monthly Electricity Demand Comparison Using ND, TSD and England Wales Demand')
plt.xlabel('Year')
plt.ylabel('Demand (MW)')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.tight_layout()
plt.show()