import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import seaborn as sns

# Read csv file
df = pd.read_csv('demanddata2009_2024_A.csv')

# Extract year and month from settlement_datetime 
df['SETTLEMENT_DATETIME'] = pd.to_datetime(df['SETTLEMENT_DATETIME'])
df['Year'] = df['SETTLEMENT_DATETIME'].dt.year
df['Month'] = df['SETTLEMENT_DATETIME'].dt.month

# Get the absolute values of the different flows 
columns_to_convert = ['IFA_FLOW', 'IFA2_FLOW', 'BRITNED_FLOW', 'MOYLE_FLOW', 
                      'EAST_WEST_FLOW', 'NEMO_FLOW', 'NSL_FLOW', 'ELECLINK_FLOW', 'VIKING_FLOW']

for column in columns_to_convert:
    df[column] = df[column].abs()

# Group by year and month 
monthly_sum = df.groupby(['Year', 'Month'])[columns_to_convert].sum().reset_index()

# Change the colour palette
colors = sns.color_palette('tab10', len(columns_to_convert))

# Plot the line graphs on a 3x3 grid 
fig, axs = plt.subplots(3, 3, figsize=(15, 10), sharex=True, sharey=True)

for i, (column, color) in enumerate(zip(columns_to_convert, colors)):
    row = i // 3
    col = i % 3
    axs[row, col].plot(monthly_sum['Year'] + monthly_sum['Month']/12, monthly_sum[column], color=color)
    axs[row, col].set_title(column)
    axs[row, col].tick_params(axis='x', rotation=45)
    
# Adjust x-axis so only years 2009 to 2024 show
plt.xticks(range(2009, 2025))

# Add title
plt.suptitle("Electricity Generated from Each UK Interconnector Over Time", fontsize=16)

# Add y-axis label
fig.text(0.005, 0.5, 'Sum of Generated Electricity (MW)', ha='center', va='center', rotation='vertical', fontsize=10)

# Add x-axis label (this overrides the x-axis so has  been commented out)
#fig.text(0.5, 0.004, 'Years', ha='center', va='center', fontsize=10)

# Change the 1e10 to a maths formats and show graph
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.tight_layout()
plt.show()