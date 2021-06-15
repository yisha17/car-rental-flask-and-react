from flask_sqlalchemy import SQLAlchemy
import sys


db = SQLAlchemy()


class Car(db.Model):
    __tablename__ = "car"
    CarID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String, nullable=False)
    CarType = db.Column(db.String, nullable=False)
    CarImage = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False                                )
    isAvailable = db.Column(db.Boolean, nullable=False)


class Customer(db.Model):
    __tablename__ = "customer"
    CustomerID = db.Column(db.Integer, primary_key=True)
    CustomerName = db.Column(db.String, nullable=False)
    CustomerEmail = db.Column(db.String, nullable=False)
    CustomerPassword = db.Column(db.String, nullable=False)
    reservations = db.relationship('Reservation',backref='customer',lazy=True)


class Reservation(db.Model):
    __tablename__ = "reservation"
    ReservationID = db.Column(db.Integer, primary_key=True)
    CarID = db.Column(db.Integer, db.ForeignKey("car.CarID"), nullable=False)
    CustomerID = db.Column(
        db.Integer, db.ForeignKey("customer.CustomerID"), nullable=False
    )
    pickup_date = db.Column(db.String, nullable=False)
    dropup_date = db.Column(db.String, nullable=False)
    Location = db.Column(db.String,nullable = False)
    
