import pandas as pd
import os

directory = 'C:/Users/niffi/OneDrive/Documents/AI and Data Science/Semester 2/Visualisation for Data Analytics/Coursework/Part II/Historic Demand Data 2009 to 2024'

#List all CSV files in the directory
csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]

#Reads the CSV files into dfs and stores in a list
dfs = []
for file in csv_files:
    df = pd.read_csv(os.path.join(directory, file))
    dfs.append(df)

#Concatenate all df into one df
combined_df = pd.concat(dfs, ignore_index=True)

#Convert 'SETTLEMENT_DATE' to the right format
combined_df['SETTLEMENT_DATE'] = pd.to_datetime(combined_df['SETTLEMENT_DATE'], format='%d-%b-%Y')

#Sort by settlement date and settlement period
combined_df.sort_values(by=['SETTLEMENT_DATE', 'SETTLEMENT_PERIOD'], inplace=True)

# Save the new csv file
combined_df.to_csv('demanddata2009_2024.csv', index=False)