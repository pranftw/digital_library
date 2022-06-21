from flask import Flask
from flask import session as flask_session
from config import HOST, PORT, DEBUG, SECRET_KEY, EMAIL_USERNAME, EMAIL_PASSWORD
from db_setup import conn_str
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)

# FLASK CONFIG
app.config['SECRET_KEY'] = SECRET_KEY

# SQLALCHEMY CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = conn_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# EMAIL CONFIG
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = EMAIL_USERNAME
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD

db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

mail = Mail(app)

import routes

if __name__=='__main__':
    app.jinja_env.cache = {}
    app.run(host=HOST, port=PORT, debug=DEBUG, threaded=True)
