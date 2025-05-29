from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)

    def __init__(self, username, password, phone_number, email, address):
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.email = email
        self.address = address

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='Active')
    start_date = db.Column(db.Date, default=date.today)
    end_date = db.Column(db.Date, default=date.today() + timedelta(days=30))

    def __init__(self, user_id, plan_id):
        self.user_id = user_id
        self.plan_id = plan_id

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_mode = db.Column(db.String(50), nullable=False)
    last_payment_date = db.Column(db.Date, default=date.today)

    def __init__(self, user_id, subscription_id, amount, payment_mode):
        self.user_id = user_id
        self.subscription_id = subscription_id
        self.amount = amount
        self.payment_mode = payment_mode

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, description, rating):
        self.user_id = user_id
        self.description = description
        self.rating = rating

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    data_limit = db.Column(db.Integer, nullable=False)
    offer = db.Column(db.String(255), nullable=True)  # New field for offers

    def __init__(self, name, price, speed, data_limit, offer=None):
        self.name = name
        self.price = price
        self.speed = speed
        self.data_limit = data_limit
        self.offer = offer