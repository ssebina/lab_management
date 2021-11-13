from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask_cors import CORS

from .momentjs import momentjs

from flask_moment import Moment



app = Flask(__name__)
app.config.from_object('config')

CORS(app, expose_headers=["x-suggested-filename", "Content-Disposition"])

app.jinja_env.globals['momentjs'] = momentjs

moment = Moment(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.sesseion_protection = 'strong'
login_manager.login_view = 'auth.login'


from app.auth import bp as auth
app.register_blueprint(auth, url_prefix='/auth')

from app.user_management import bp as user_management
app.register_blueprint(user_management, url_prefix='/user_management')

from app.equipment_management import bp as equip
app.register_blueprint(equip, url_prefix='/equipment_management')



from app.hospital_management import bp as hospital
app.register_blueprint(hospital, url_prefix='/hospital_management')


from app import views, models