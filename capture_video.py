import csv
from qscript import CaptureVideo_Magento

with open('input.csv', 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';')

    next(csv_reader)

    for row in csv_reader:
        if not row:
            continue
            
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