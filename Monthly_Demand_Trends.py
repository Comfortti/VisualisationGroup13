import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv("demanddata2009_2024_A.csv")

# Convert SETTLEMENT_DATETIME to datetime format
df['SETTLEMENT_DATETIME'] = pd.to_datetime(df['SETTLEMENT_DATETIME'])

# Extract year and month from SETTLEMENT_DATETIME
df['Year'] = df['SETTLEMENT_DATETIME'].dt.year
df['Month'] = df['SETTLEMENT_DATETIME'].dt.month

# Create a stacked boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(x='Month', y='value', hue='variable', data=pd.melt(df, id_vars=['Year', 'Month'], value_vars=['ND', 'TSD', 'ENGLAND_WALES_DEMAND']))

# Have labels and title
plt.xlabel('Month')
plt.ylabel('Demand (MW)')
plt.title('Demand by Month')

# Show the plot
plt.legend(title='Type of Demand')
plt.show()
