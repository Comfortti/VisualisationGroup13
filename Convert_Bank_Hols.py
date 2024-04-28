import pandas as pd

df = pd.read_csv("Bank_Hols_2009_2024.csv")

#Convert the date from DD/MM/YYYY to YYYY-MM-DD
df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

# Save new csv file
df.to_csv("Bank_Hols_2009_2024_updated.csv", index=False)

print("Date Conversion Completed")
