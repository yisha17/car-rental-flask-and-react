from logging import error
from re import T
from flask import Blueprint,request
from flask.json import jsonify
from marshmallow.fields import String
from flask_restx import Resource,Api,fields
from . import db,API
from .ma import *
from .models import Car,Customer,Reservation
from sqlalchemy.orm import sessionmaker 
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_cors import cross_origin




bp = Blueprint('tasks',__name__)

car_schema = CarsSchema()
cars_schema = CarsSchema(many=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

rv_schema = ReservationSchema()
rvs_schema = ReservationSchema(many=True)




car = API.model("Car",{
    'CarName': fields.String,
    'CarType': fields.String,
    'CarImage': fields.String,
    'isAvailable':fields.Boolean
})

customer = API.model("Customer",{
    'CustomerID':fields.Integer,
    'CustomerName':fields.String,
    'CustomerEmail':fields.String,
    'CustomerPassword':fields.String
})

user = API.model("Customer",{
    'CustomerID':fields.Integer,
    'CustomerName':fields.String,
    'CustomerPassword':fields.String
})

reservation = API.model("Reservation",{
    'CarID':fields.Integer,
    'CustomerID':fields.Integer,
    'pickup_date':fields.DateTime,
    'dropup_date':fields.DateTime,
    'Location':fields.String,
    'price':fields.Integer
})

@API.route("/api/cars/<int:id>")
class CarResource(Resource):
    def get(self,id):
        car = Car.query.filter_by(CarID = id).first()
        if car is None:
            return None,404
        return car_schema.dump(car)
    
    
    @API.expect(car)
    @API.response(204,'Car Successfully updated')
    def put(self,id):
        car = Car.query.filter_by(CarID = id).first()
        
        car.CarName = request.json['CarName']
        car.CarType = request.json['CarType']
        car.CarImage = request.json['CarImage']
        car.isAvailable = True
        
        db.session.add(car)
        db.session.commit()
        
        return cars_schema.dump(car)   
        
    
    
    @API.response(204, 'Car successfully deleted.')
    def delete(self, id):    
        car = Car.query.filter_by(CarID = id).first()
        if car is None:
            return None,204
        db.session.delete(car)
        db.session.commit()
        return None, 204
    
@API.route("/api/cars")
class CarsResource(Resource):
    def get(self):
        car = Car.query.all()
        return cars_schema.dump(car)
    
    

@API.route('/api/reservation/<int:id>')    
class ReservationResource(Resource):
    
    def get(self,id):
        rv = Reservation.query.filter_by(ReservationID = id).first()
        if rv is None:
            return None,404
        return rv_schema.dump(rv)
    
    @API.expect(reservation)
    @API.response(204,'Car Successfully updated')
    def put(self,id):
        rv = Reservation.query.filter_by(ReservationID = id).first()
        
        rv.CarID = request.json['CarID']
        rv.CustomerID = request.json['CustomerID']
        rv.pickup_date = request.json['pickup_date']
        rv.dropup_date = request.json['dropup_date']
        rv.Location = request.json['Location']
        rv.price = request.json['price']
         
        
        db.session.add(rv)
        db.session.commit()
        
        return rv_schema.dump(rv) 
    
    @API.response(204, 'Reservation successfully deleted.')
    def delete(self, id):    
        rv = Reservation.query.filter_by(ReservationID = id).first()
        if rv is None:
            return None,204
        db.session.delete(rv)
        db.session.commit()
        return None, 204
    
@API.route('/api/reservation')
class ReservationsResource(Resource):        
    def get(self):
        rv = Reservation.query.all()
        return rvs_schema.dump(rv)
    
    def post(self):
        rv = Reservation()
        rv.CarID = request.json['CarID']
        rv.CustomerID = request.json['CustomerID']
        rv.pickup_date = request.json['pickup_date']
        rv.dropup_date = request.json['dropup_date']
        rv.Location = request.json['Location']
        rv.price = request.json['price']
         
        
        db.session.add(rv)
        db.session.commit()
        
        return rv_schema.dump(rv)

@API.route('/api/customer/<int:id>')    
class CustomerResource(Resource):
    
    def get(self,id):
        user = Customer.query.filter_by(ReservationID = id).first()
        return customer_schema.dump(user)
    
    @API.expect(customer)
    @API.response(204,'Customer Successfully updated')
    def put(self,id):
        user = Customer.query.filter_by(CustomerID = id).first()
        user.CustomerName= request.json['CustomerName']
        user.CustomerEmail = request.json['CustomerEmail']
        user.CustomerPassword = request.json['CustomerPassword']
         
        db.session.add(user)
        db.session.commit()
        
        return rv_schema.dump(user) 
    
    @API.response(204, 'customer successfully deleted.')
    def delete(self, id):    
        user = Customer.query.filter_by(ReservationID = id).first()
        if user is None:
            return None,204
        db.session.delete(user)
        db.session.commit()
        return None, 204
    
@API.route('/api/customer')
class CustomersResource(Resource):        
    def get(self):
        user = Customer.query.all()
        return rvs_schema.dump(user)
    @API.expect(customer)
    def post(self):
        user = Customer()
        user.CustomerName = request.json['CustomerName']
        user.CustomerPassword = request.json['CustomerPassword']
        if user.CustomerName != "test" or user.CustomerPassword != "test":
            return jsonify({"msg": "Bad username or password"}), 401
        
        return customer_schema.dump(customer_schema)
    
    @API.expect(user)
    @cross_origin()
    def post(self):
        user = Customer()
        user.CustomerName = request.json['CustomerName']
        print(user.CustomerName)
        user.CustomerPassword = request.json['CustomerPassword']
        
        user_check = Customer.query.filter_by(CustomerName = user.CustomerName).filter_by(CustomerPassword = user.CustomerPassword).first()
        print(user_check == None)
        if user_check == None:
            return jsonify({"msg":"it is not successful"})
        else:
            access_token = create_access_token(identity = user.CustomerName)
            return jsonify(CustomerID = user_check.CustomerID, access_token = access_token)
        

