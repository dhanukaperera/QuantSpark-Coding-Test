from flask import  request, jsonify
from app import app, models, calculate_movement, get_previous_business_day
import datetime
import logging

logger = logging.getLogger()

@app.route('/')
@app.route('/index')
def index():
    return "App is Running!"

@app.route('/movements',methods = ['POST'])
def movements():
    business_date = request.args.get('date')
    if not business_date:
        logger.error("Missing date parameter")
        return jsonify(error='Missing date parameter'), 400

    try:
        business_date = datetime.datetime.strptime(business_date, '%d/%m/%Y').date()
    except ValueError:
        logger.error("Invalid date parameter: {}".format(business_date))
        return jsonify(error='Invalid date parameter'), 400

    previous_day = get_previous_business_day(business_date)
    current_rates = models.FXRate.query.filter_by(business_date=business_date).all()
    previous_rates = models.FXRate.query.filter_by(business_date=previous_day).all()

    if not current_rates or not previous_rates:
        logger.warning("No data for the given date: {}".format(business_date))
        return jsonify(error='No data for the given date'), 404

    movements = []
    for current_rate in current_rates:
        previous_rate = next((r for r in previous_rates if r.currency_code == current_rate.currency_code), None)
        if previous_rate:
            movement = calculate_movement(current_rate.exchange_rate, previous_rate.exchange_rate)
            current_rate.movement = movement
            movements.append(current_rate.to_dict())

    return jsonify(movements)