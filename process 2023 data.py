import csv
import re
from datetime import datetime

def remove_punctuation(text):
    return re.sub('[^a-zA-Z0-9\s]', '', text)

def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%d-%b-%Y')

def process_csv(input_file, output_file):
    with open(input_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        data = [header]
        for row in reader:
            row[1] = remove_punctuation(row[1])  
            row[0] = convert_date_format(row[0])
            data.append(row)

    with open(output_file, 'w', newline='') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerows(data)

input_file = 'demanddata_2023.csv'
output_file = 'processed_demanddata_2023.csv'
process_csv(input_file, output_file)
print("CSV processing has finished.")