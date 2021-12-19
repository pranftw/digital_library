from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import SECRET_KEY
from hashlib import sha256
from __main__ import mail
from flask_mail import Message
import datetime as dt
from datetime import timedelta
import re

def hash_password(pswd):
    return sha256(pswd.encode('utf-8')).hexdigest()

def send_reset_email(email, reset_url):
    msg = Message('Password Reset Request', sender='noreply@bmscelib.com',recipients=[email])
    msg.body = f"""To reset your password, click on the following link!

    {reset_url}
    """
    mail.send(msg)

def send_notify_email(emails, book_obj, home_url):
    msg = Message('Book available notification!', sender='noreply@bmscelib.com',recipients=emails)
    msg.body = f"""The book you requested {book_obj.title} by {book_obj.author} is now available!
    Number of stocks left are {book_obj.stocks}.
    Click the following link to be able to issue the book!
    
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

def validate_email(email):
    pattern = re.compile(r'[a-zA-Z.0-9]+@bmsce.ac.in')
    match = pattern.match(email)
    if match:
        return True
    return False

def validate_password(password):
    lowercase = re.compile(r'[a-z]+')
    uppercase = re.compile(r'[A-Z]+')
    nums = re.compile(r'[0-9]+')
    match = lowercase.match(password) and uppercase.match(password) and nums.match(password)
    if match:
        return True
    return False

def validate_name(name):
    pattern = re.compile(r'^[a-zA-Z\s]+$')
    match = pattern.match(name)
    if match:
        return True
    return False

def validate_sem(sem):
    try:
        sem = int(sum)
        if sem in range(3-9):
            return True
    except:
        pass
    return False

def validate_form_data(form_data):
    errors = []
    for k,v in form_data.items():
        if k=='first_name' or k=='last_name' or k=='title' or k=='author':
            if not(validate_name(v)):
               errors.append(f"Enter a valid value for {k}!")
        elif k=='email':
            if not(validate_email(v)):
                errors.append("Enter a valid BMSCE email!")
        elif k=='password':
            if not(validate_password(v)):
                errors.append("Enter atleast one lowercase, one uppercase and one digit!")
        elif k=='confirm_password':
            if(not(form_data['password']==form_data['confirm_password'])):
                errors.append("Both the passwords must match!")
        elif k=='sem':
            if not(validate_sem(v)):
                errors.append("Semester should be in between 3 and 8(both inclusive)!")
    return errors
