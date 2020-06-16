import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from nustiu.camera.camera import mod3
from nustiu.medic.medic import mod1
# from nustiu.general.general import mod2
from nustiu.patient.patient import mod2
from nustiu.admin.admin import mod4
from utils.Util import *

# from controller.MedicController import medic
from utils.extensions import db


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
Bootstrap(app)


db.init_app(app)
login = LoginManager(app)
login.login_view = 'login'
app.app_context().push()

app.register_blueprint(mod2)
app.register_blueprint(mod1)
app.register_blueprint(mod3)
app.register_blueprint(mod4)

if __name__ == '__main__':
    from nustiu.general.general import *
    # from routes import *

    app.run( debug=True)
