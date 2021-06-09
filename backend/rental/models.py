from flask_sqlalchemy import SQLAlchemy
import sys


db = SQLAlchemy()


class Cars(db.Model):
    __tablename__ = "cars"
    CarID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String, nullable=False)
    CarType = db.Column(db.String, nullable=False)
    CarImage = db.Column(db.String, nullable=False)
    isAvailable = db.Column(db.Boolean, nullable=False)


class Customer(db.Model):
    __tablename__ = "customer"
    CustomerID = db.Column(db.Integer, primary_key=True)
    CustomerName = db.Column(db.String, nullable=False)
    CustomerEmail = db.Column(db.String, nullable=False)
    CustomerPassword = db.Column(db.String, nullable=False)


class Reservation(db.Model):
    __tablename__ = "reservation"
    ReservationID = db.Column(db.Integer, primary_key=True)
    CarID = db.Column(db.Integer, db.ForeignKey("cars.CarID"), nullable=False)
    CustomerID = db.Column(
        db.Integer, db.ForeignKey("customer.CustomerID"), nullable=False
    )
    pickup_date = db.Column(db.DateTime, nullable=False)
    dropup_date = db.Column(db.DateTime, nullable=False)
    Location = db.Column(db.String,nullable = False)
    price = db.Column(db.Integer, nullable=False)
