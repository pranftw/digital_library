from __main__ import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users'

class Book(db.Model):
    __tablename__='books'

class Issued(db.Model):
    __tablename__='issued'

class Notify(db.Model):
    __tablename__='notify'

class Requests(db.Model):
    __tablename__='requests'

class ToBeApproved(db.Model):
    __tablename__='to_be_approved'
