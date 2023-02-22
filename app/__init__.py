from flask import Flask ,request, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def get_previous_business_day(business_date):
    previous_day = business_date - datetime.timedelta(days=1)
    if previous_day.weekday() in (5, 6):
        return get_previous_business_day(previous_day)
    return previous_day

def calculate_movement(current_rate, previous_rate):
    return (1 - (current_rate / previous_rate)) * 100

@app.route('/movements',methods = ['POST'])
def movements():
    business_date = request.args.get('date')
    if not business_date:
        return jsonify(error='Missing date parameter'), 400

    try:
        business_date = datetime.datetime.strptime(business_date, '%d/%m/%Y').date()
    except ValueError:
        return jsonify(error='Invalid date parameter'), 400

    previous_day = get_previous_business_day(business_date)
    current_rates = models.FXRate.query.filter_by(business_date=business_date).all()
    previous_rates = models.FXRate.query.filter_by(business_date=previous_day).all()

    if not current_rates or not previous_rates:
        return jsonify(error='No data for the given date'), 404

    movements = []
    for current_rate in current_rates:
        previous_rate = next((r for r in previous_rates if r.currency_code == current_rate.currency_code), None)
        if previous_rate:
            movement = calculate_movement(current_rate.exchange_rate, previous_rate.exchange_rate)
            current_rate.movement = movement
            movements.append(current_rate.to_dict())

    return jsonify(movements)

from app import routes, models