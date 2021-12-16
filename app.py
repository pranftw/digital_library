from flask import Flask
from flask import session as flask_session
from config import HOST, PORT, DEBUG, SECRET_KEY
from db_setup import conn_str
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = conn_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

import routes

if __name__=='__main__':
    app.jinja_env.cache = {}
    app.run(host=HOST, port=PORT, debug=DEBUG, threaded=True)
