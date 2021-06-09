import os



from .models import Customer

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental.db'
print("database created")
app.config['SECRET_KEY'] ='JBER34N342'
app.config['FLASK_DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

db = SQLAlchemy(app)
API = Api(app)

guard = flask_praetorian.Praetorian()
cors = flask_cors.CORS()