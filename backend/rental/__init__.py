import os

from flask import Flask, jsonify

from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from .models import db
from .extension import jwt,admin,cors,migrate,mail
from flask_admin.contrib.sqla import ModelView

from .models import *

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental.db'
print("database created")
app.config['SECRET_KEY'] ='JBER34N342'
app.config['FLASK_DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['JWT_SECRET_KEY'] = 'NJ4TU4FNJ4MS'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'it.yisak.wondim@gmail.com'
app.config['MAIL_PASSWORD'] = 'yisak273954'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True  



db.init_app(app)
jwt.init_app(app)
cors.init_app(app)
admin.init_app(app)
migrate.init_app(app,db)
mail.init_app(app)
API = Api(app)

admin.add_view(ModelView(Car,db.session))
admin.add_view(ModelView(Customer,db.session))
admin.add_view(ModelView(Reservation,db.session))

with app.app_context():
    db.create_all()
  

from . import api

app.register_blueprint(api.bp)
