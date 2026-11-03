import csv
from qscript.py import CaptureVideo_Magento

with open('input.csv', 'r') as csvfile:
    csv_reaader = csv.reader(csvfile)

    next(csv.reader)

    for row in csv_reaader:
        url = row[0]
        company_name = row[1]
        language = row[2]
        country = row[3]
        postcode = row[4]
        city = row[5]
        street = row[6]
        house_no = row[7]

        CaptureVideo_Magento(
            url,
            company_name,
            language,
            country,
            postcode,
            city,
            street,
            house_no
        )