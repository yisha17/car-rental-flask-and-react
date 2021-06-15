from logging import error
from re import T
from flask import Blueprint,request
from flask.json import jsonify
from marshmallow.fields import String
from flask_restx import Resource,Api,fields
from . import db,API,mail
from .ma import *
from .models import Car,Customer,Reservation
from sqlalchemy.orm import sessionmaker 
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_cors import cross_origin
from flask_mail import Mail, Message




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
     'price': fields.Integer,
    'isAvailable':fields.Boolean
})

customer = API.model("Customer",{
    'CustomerID':fields.Integer,
    'CustomerName':fields.String,
    'CustomerEmail':fields.String,
    'CustomerPassword':fields.String,
    'reservations':fields.Nested(rvs_schema)
})

user = API.model("Customer",{
    'CustomerID':fields.Integer,
    'CustomerName':fields.String,
    'CustomerPassword':fields.String
})

reservation = API.model("Reservation",{
    'ReservationID': fields.Integer,
    'CarID':fields.Integer,
    'CustomerID':fields.Integer,
    'pickup_date':fields.String,
    'dropup_date':fields.String,
    'Location':fields.String,
    'msg':'successful'
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
        rv.CarID
        car = Car.query.filter_by(CarID = rv.CarID).first()
        user = Customer.query.filter_by(CustomerID = rv.CustomerID).first()
        username = user.CustomerName
        car_name = car.CarName
        car_price = car.price
        car_img = car.CarImage
        pick = rv.pickup_date
        drop = rv.dropup_date
        total = int(pick[-2:]) - int(drop[-2:]) * car_price
        
        
        
        
        if rv is None:
            return None,404
        return jsonify(username= username,car_name=car_name,car_img=car_img,pick = pick,drop=drop,total=total)
    
    @API.expect(reservation)
    @API.response(204,'Car Successfully updated')
    def put(self,id):
        rv = Reservation.query.filter_by(ReservationID = id).first()
        
        rv.CarID = request.json['CarID']
        rv.CustomerID = request.json['CustomerID']
        rv.pickup_date = request.json['pickup_date']
        rv.dropup_date = request.json['dropup_date']
        rv.Location = request.json['Location']
        
         
        
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
        car = Car()
        user = Customer()
        rv.CarID = request.json['CarID']
        rv.CustomerID = request.json['CustomerID']
        rv.pickup_date = request.json['pickup_date']
        rv.dropup_date = request.json['dropup_date']
        rv.Location = request.json['Location']
        
        
        if (rv.CarID == '' or rv.CustomerID == '' or rv.Location == '' ):
            return jsonify({'msg':'it is not successful'})
        else:
            db.session.add(rv)
            db.session.commit()
            
            car = Car.query.filter_by(CarID = rv.CarID).first()
            car.isAvailable = False
            db.session.commit()
            
            name = Customer.query.filter_by(CustomerID = rv.CustomerID).first()
            first = name.CustomerName
            email = name.CustomerEmail
            pdate = rv.pickup_date
            ddate = rv.dropup_date
            
            msg = Message('hello {}'.format(name.CustomerName),sender='it.yisak.wondim@gmail.com',recipients =['it.yisak.wondim@gmail.com'])
            msg.body = f'Hi {first} you successfully reserve a car. you have to pick your car on {pdate} and return the car on {ddate}. Thanks'
            mail.send(msg)
        
            return rv_schema.dump(rv)
        
         
        
        

@API.route('/api/customer/<int:id>')    
class CustomerResource(Resource):
    
    def get(self,id):
        user = Customer.query.filter_by(CustomerID = id).first()
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
    
    
    
    @API.expect(user)
    @cross_origin()
    def post(self):
        user = Customer()
        user.CustomerName = request.json['CustomerName']
        user.CustomerPassword = request.json['CustomerPassword']
        msg = 'successful'
        user_check = Customer.query.filter_by(CustomerName = user.CustomerName).filter_by(CustomerPassword = user.CustomerPassword).first()
        if user_check == None:
            return jsonify({"msg":"it is not successful"})
        else:
            access_token = create_access_token(identity = user.CustomerName)
            return jsonify(CustomerID = user_check.CustomerID, access_token = access_token,msg=msg)

@API.route('/api/register/customer')        
class UserResource(Resource): 
    def post(self):
        try:
            user = Customer()
            user.CustomerName= request.json['CustomerName']
            user.CustomerEmail = request.json['CustomerEmail']
            user.CustomerPassword = request.json['CustomerPassword']
            
            db.session.add(user)
            db.session.commit()
            
            return rv_schema.dump(user)
        except:
            return jsonify({"msg":"not successful"},404)

        
        
               
        

