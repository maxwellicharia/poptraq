from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, Manager, MigrateCommand
from flask_bootstrap import Bootstrap
from flask_debug import Debug
from flask_mail import Mail
from flask_recaptcha import ReCaptcha
from flask_socketio import SocketIO
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://9893fa47a103437785f3f1bb07f81835@sentry.io/1302450",
    integrations=[FlaskIntegration()],
    max_breadcrumbs=50,
    debug=True
)

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='anyapp8@gmail.com',
    MAIL_PASSWORD='anyapp8#@123',
    MAIL_DEFAULT_SENDER = "anyapp8@gmail.com",

    RECAPTCHA_ENABLED=True,
    RECAPTCHA_PUBLIC_KEY="6LfgSHMUAAAAAPCT_9i_stHIR_AxowHyHvF-oD0z",
    RECAPTCHA_PRIVATE_KEY="6LfgSHMUAAAAAEhiNnOEep3jwRgATmKsdmjEpbl_",
    RECAPTCHA_THEME="dark",
    RECAPTCHA_TYPE="image",
    RECAPTCHA_SIZE="compact",
    RECAPTCHA_RTABINDEX=10,
    RECAPTCHA_PARAMETERS={'hl': 'en-GB'},

    SECRET_KEY="$poptraq#",
    SECURITY_PASSWORD_SALT="@tre3potraq#",
    # SQLALCHEMY_DATABASE_URI="postgres://unjltzspnbvjzb:e511c61dacd775cffc0857dde01511955532ef8b08c88c897b0d21b874f94848"
    #                         "@ec2-54-221-251-195.compute-1.amazonaws.com:5432/d1lqqk8qoqodln",
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/potraq",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    BCRYPT_LOG_ROUNDS=13,
    WTF_CSRF_ENABLED=True

)

app.config.update(dict(
    RECAPTCHA_SITE_KEY="public",
    RECAPTCHA_SECRET_KEY="private",
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u"Login required to gain access"
login_manager.login_message_category = "info"

bootstrap = Bootstrap(app)

Debug(app)

mail = Mail(app)

db = SQLAlchemy(app)

socketio = SocketIO(app)


from poptraq.models import User, County
from poptraq import views
from poptraq.views import admin, user, views

manager = Manager(app)
manager.add_command('db', MigrateCommand)

migrate = Migrate(app, db)
