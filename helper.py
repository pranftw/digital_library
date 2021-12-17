from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import SECRET_KEY
from hashlib import sha256
from __main__ import mail
from flask_mail import Message
import datetime as dt
from datetime import timedelta

def hash_password(pswd):
    return sha256(pswd.encode('utf-8')).hexdigest()

def send_reset_email(email, reset_url):
    msg = Message('Password Reset Request', sender='noreply@bmscelib.com',recipients=[email])
    msg.body = f"""To reset your password, click on the following link!
        {reset_url}
    """
    mail.send(msg)

def send_notify_email(email, book_obj, home_url):
    msg = Message('Book available notification!')
    msg.body = f"""The book you requested {book.title} by {book.author} is now available!
    Number of stocks left are {book.stocks}.
    Click the following link to be able to issue the book from your watchlist!
        {home_url}
    """
    mail.send(msg)

def get_token(user):
    s = Serializer(SECRET_KEY, 300)
    token = s.dumps(f"{user.email}").decode('utf-8')
    return token

def validate_token(token):
    s = Serializer(SECRET_KEY)
    try:
        payload = s.loads(token)
        return payload
    except:
        return None

def get_due_date(issue_date):
    issue_date_obj = issue_date
    due_date_obj = issue_date_obj + timedelta(days=15)
    curr_date_obj = dt.datetime.now()
    diff = curr_date_obj - due_date_obj
    diff_days = diff.days
    due_date_str = due_date_obj.strftime('%d-%m-%Y')
    return due_date_str, diff_days

