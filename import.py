import csv
import datetime
from app import app, db, models

def import_csv():
    with open('/Users/dhanukaperera/Projects/QuantSpark/data/fx_rates_1720230124.csv',mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
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

with app.app_context():
    import_csv()
