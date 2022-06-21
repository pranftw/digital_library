from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import SECRET_KEY
from hashlib import sha256
from __main__ import mail
from flask_mail import Message
import datetime as dt
from datetime import timedelta
from config import EMAIL_USERNAME
import re

def hash_password(pswd):
    return sha256(pswd.encode('utf-8')).hexdigest()

def send_reset_email(email, reset_url):
    msg = Message('Password Reset Request', sender=EMAIL_USERNAME,recipients=[email])
    msg.body = f"""To reset your password, click on the following link!

    {reset_url}
    """
    mail.send(msg)

def send_notify_email(emails, book_obj, url):
    if len(emails)!=0:
        msg = Message('Book available notification!', sender=EMAIL_USERNAME,recipients=emails)
        msg.body = f"""The book you requested {book_obj.title} by {book_obj.author} is now available!
        Number of stocks left are {book_obj.stocks}.
        Click the following link to be able to issue the book!
        
        {url}
        """
        mail.send(msg)

def send_verification_email(email, verification_token):
    msg = Message('Verification code', sender=EMAIL_USERNAME, recipients=[email])
    msg.body = f"""The verification code for your registration with BMSCE Lib is {verification_token}
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
    pattern = re.compile(r'[a-zA-Z.0-9]+@bmsce\.ac\.in')
    match = pattern.match(email)
    if match:
        return True
    return False

def validate_password(password):
    lowercase = re.compile(r'.*[a-z]+.*')
    uppercase = re.compile(r'.*[A-Z]+.*')
    nums = re.compile(r'.*[0-9]+.*')
    lowercase_match = True if lowercase.match(password) else False
    uppercase_match = True if uppercase.match(password) else False
    nums_match = True if nums.match(password) else False
    match = lowercase_match and uppercase_match and nums_match
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
        sem = int(sem)
        if sem in range(3,9):
            return True
    except:
        pass
    return False

def validate_form_data(form_data):
    errors = []
    for k,v in form_data.items():
        if k=='first_name' or k=='last_name' or k=='title' or k=='author' or k=='subject':
            if not(validate_name(v)):
               errors.append(f"Enter a valid value for {k}!")
        elif k=='email':
            if not(validate_email(v)):
                errors.append("Enter a valid BMSCE email!")
        elif k=='password':
            if not(validate_password(v)):
                errors.append("Enter atleast one lowercase, one uppercase and one digit in the password!")
        elif k=='confirm_password':
            if(not(form_data['password']==form_data['confirm_password'])):
                errors.append("Both the passwords must match!")
        elif k=='sem':
            if not(validate_sem(v)):
                errors.append("Semester should be in between 3 and 8(both inclusive)!")
    return errors
