from flask_marshmallow import Marshmallow
from .models import *

from . import app
ma = Marshmallow(app)


class CarsSchema(ma.Schema):
    class Meta:
        fields = ("CarID","CarName","CarType","CarImage","price","isAvailable")
        model = Car

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ("CustomerID","CustomerName","CustomerEmail","CustomerPassword")
        model = Customer

class ReservationSchema(ma.Schema):
    class Meta:
        fields = ("ReservationID","CarID","CustomerID","pickup_date","dropup_date","Location")
        model = Reservation                
        
        