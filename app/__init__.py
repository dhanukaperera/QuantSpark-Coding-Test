from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
import logging

logger = logging.getLogger()

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def get_previous_business_day(business_date):
    try:
        previous_day = business_date - datetime.timedelta(days=1)
        if previous_day.weekday() in (5, 6):
            return get_previous_business_day(previous_day)
        return previous_day
    except TypeError:
        logger.error("Invalid input provided: {}".format(business_date))
        return None

def calculate_movement(current_rate, previous_rate):
    return (1 - (current_rate / previous_rate)) * 100

from app import routes, models