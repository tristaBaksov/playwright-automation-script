import csv
from qscript import CaptureVideo_Magento

with open('input.csv', 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')

    for row in csv_reader:
            
        path = CaptureVideo_Magento(
            row['URL'],
            row['Company Name'],
            row['Language'],
            row['Country'],
            row['Postcode'],
            row['City'],
            row['Street'],
            row['HouseNo']
        )
        print(f"Saved: {path}")