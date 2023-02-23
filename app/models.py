from app import db
class FXRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_date = db.Column(db.Date)
    country_name = db.Column(db.String(50))
    currency_code = db.Column(db.String(3))
    exchange_rate = db.Column(db.Float)

    def to_dict(self):
        return {'currency_code': self.currency_code, 'movement': self.movement}
