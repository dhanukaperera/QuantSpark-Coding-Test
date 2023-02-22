from app import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class FXRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_date = db.Column(db.Date)
    country_name = db.Column(db.String(50))
    currency_code = db.Column(db.String(3))
    exchange_rate = db.Column(db.Float)

    def to_dict(self):
        return {'currency_code': self.currency_code, 'movement': self.movement}
