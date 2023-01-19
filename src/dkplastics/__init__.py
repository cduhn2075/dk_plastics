"""The dkplastics library."""
# We disable a Flake8 check for "Module imported but unused (F401)" here because
# although this import is not directly used, it populates the value
# package_name.__version__, which is used to get version information about this
# Python package.

# Local packages
import logging
# Third party packages
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_recaptcha import ReCaptcha

# cisagov Libraries
from dkplastics.data.config import config

from ._version import __version__  # noqa: F401

params = config()
login_manager = LoginManager()
# Flask implementation
app = Flask(__name__)
app.config["SECRET_KEY"] = "bozotheclown"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f'postgresql+psycopg2://{params["user"]}:{params["password"]}@{params["host"]}:{params["port"]}/{params["database"]}'
app.config['UPLOAD_FOLDER'] = "src/dkplastics/uploads/"
app.config['ALLOWED_EXTENSIONS'] = {"jpeg", "png", "jpg"}



# RECAPTCHA_ENABLED = True
app.config['RECAPTCHA_SITE_KEY'] = "6LcDP8kfAAAAAF6805Nm37Gy2jGrNofJe64_vtpZ"
app.config['RECAPTCHA_SECRET_KEY'] = "6LcDP8kfAAAAAMKz9pakTMCjPTlSVmfPl0BpQ7lZ"
app.config['RECAPTCHA_THEME'] = "dark"
app.config['RECAPTCHA_TYPE'] = "image"
app.config['RECAPTCHA_SIZE'] = "compact"
app.config['RECAPTCHA_LANGUAGE'] = "en"
app.config['RECAPTCHA_RTABINDEX'] = 10

recaptcha = ReCaptcha(app=app)

# Config DB
db = SQLAlchemy(app)
Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = "login"

__all__ = ["dkplastics"]

from dkplastics.manage_login.views import manage_login_blueprint
from dkplastics.home.views import home_blueprint

# Stakeholder views
from dkplastics.stakeholder.views import stakeholder_blueprint

# Register the flask apps
app.register_blueprint(stakeholder_blueprint)
app.register_blueprint(manage_login_blueprint)
app.register_blueprint(home_blueprint)

if __name__ == "__main__":
    logging.info("The program has started...")
    app.run(host='0.0.0.0', debug=True, port=8000)
