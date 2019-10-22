from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Seria


def set_token(user_id, email):
    s = Seria(secret_key=settings.SECRET_KEY, expires_in=3600)

    data = {
        "id": user_id,
        "email": email
    }

    data_s = s.dumps(data)
    return "http://www.meiduo.site:8000/emailsactive/?token=%s" % data_s.decode()


def get_token(token_id):
    s = Seria(secret_key=settings.SECRET_KEY, expires_in=3600)
    try:
        token_id = s.loads(token_id)
    except:
        return None
    return token_id
