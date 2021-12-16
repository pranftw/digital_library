from __main__ import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users'