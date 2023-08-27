from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Customer(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(200))
    firstname=db.Column(db.String(100))
    lastname=db.Column(db.String(100))
    govname=db.Column(db.String(100))
    phonenumber=db.Column(db.String(15))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(300))
    social_security_number = db.Column(db.String(20))
    accounts = relationship('Account', backref='customer', lazy=True)

class Roles(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100),unique=True)
    role=db.Column(db.String(100))

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    account_type = db.Column(db.String(50))
    account_number = db.Column(db.String(20))
    account_balance = db.Column(db.Float)
    date_opened = db.Column(db.DateTime, default=func.now())
    status = db.Column(db.String(50))
    transactions = relationship('Transaction', backref='account', lazy=True)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    transaction_type = db.Column(db.String(50))
    transaction_amount = db.Column(db.Float)
    transaction_datetime = db.Column(db.DateTime)
    description = db.Column(db.String(200))

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    card_type = db.Column(db.String(50))
    card_number = db.Column(db.String(20))
    expiration_date = db.Column(db.Date)
    cvv = db.Column(db.String(10))
    daily_transaction_limit = db.Column(db.Float)


class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100))
    location = db.Column(db.String(200))
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    contact_information = db.Column(db.String(100))

class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(50))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
   
class Beneficiary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    beneficiary_name = db.Column(db.String(100))
    relationship = db.Column(db.String(50))
    account_number = db.Column(db.String(20))
    bank_information = db.Column(db.String(200))

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    loan_type = db.Column(db.String(50))
    loan_amount = db.Column(db.Float)
    interest_rate = db.Column(db.Float)
    loan_term = db.Column(db.Integer)
    date_approved = db.Column(db.DateTime, default=func.now())
    status = db.Column(db.String(50))

class Statement_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address=db.Column(db.String(100))
    from_date = db.Column(db.DateTime)
    to_date = db.Column(db.DateTime)
    file_password=db.Column(db.String(100))
    request_datetime = db.Column(db.DateTime)
    user_email_id = db.Column(db.String(100), db.ForeignKey('customer.email'), nullable=False)


