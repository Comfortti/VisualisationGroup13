import pandas as pd

demand_data = pd.read_csv("demanddata2009_2024.csv")

#Read the bank holidays CSV
bank_holidays = pd.read_csv("Bank_Hols_2009_2024.csv")

#Convert dates to datetime
demand_data['SETTLEMENT_DATE'] = pd.to_datetime(demand_data['SETTLEMENT_DATE'])
bank_holidays['DATE'] = pd.to_datetime(bank_holidays['DATE'])

#Merge the demand data with bank holidays based on dates
merged_data = pd.merge(demand_data, bank_holidays, how='left', left_on='SETTLEMENT_DATE', right_on='DATE')

#Create a new column 'IS_HOLIDAY' initialised with 0
merged_data['IS_HOLIDAY'] = 0

#Mark the rows where the date matches a holiday as 1
merged_data.loc[merged_data['DATE'].notnull(), 'IS_HOLIDAY'] = 1

#Drop the redundant 'DATE' column
merged_data.drop('DATE', axis=1, inplace=True)

#Save the updated csv file
merged_data.to_csv("demanddata2009_2024_with_holidays.csv", index=False)