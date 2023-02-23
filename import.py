import csv
import glob
import datetime
from app import app, db, models
import datetime

csv_directory = './data'

csv_files = glob.glob(csv_directory + '/*.csv')

headers = ['business_date', 'country_name', 'currency_code', 'exchange_rate']

def import_csv():
    for csv_file in csv_files:
        with open(csv_file,mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            header_row = next(reader)

            if all(header in header_row for header in headers):
                print('All headers exist in the CSV file')
                for row in reader:
                    try:
                        business_date = datetime.datetime.strptime(row['business_date'], '%d/%m/%Y').date()
                        exchange_rate = float(row['exchange_rate'])
                        fxrate = models.FXRate(business_date=business_date, country_name=row['country_name'], 
                                    currency_code=row['currency_code'], exchange_rate=exchange_rate)
                        db.session.add(fxrate)
                    except (ValueError, TypeError):
                        app.logger.warning(f"Invalid data: {row}")
                db.session.commit()
            else:
                missing_headers = [header for header in headers if header not in header_row]
                print('The following headers are missing in the CSV file {} : {}'.format(csv_file, missing_headers))

with app.app_context():
    import_csv()
