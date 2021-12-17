from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import SECRET_KEY
from hashlib import sha256
from __main__ import mail
from flask_mail import Message

def hash_password(pswd):
    return sha256(pswd.encode('utf-8')).hexdigest()

def send_reset_email(email, reset_url):
    msg = Message('Password Reset Request', sender='noreply@bmscelib.com',recipients=[email])
    msg.body = f"""To reset your password, click on the following link!
        {reset_url}
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