from flask import app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_admin import Admin
from flask_cors import CORS
from flask_migrate import Migrate
from flask_mail import Mail

admin = Admin()
jwt = JWTManager()
cors = CORS()
migrate = Migrate()
mail = Mail()

