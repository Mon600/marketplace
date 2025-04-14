from datetime import datetime, timezone, timedelta

from jose import jwt, JWTError

from config import get_auth_data


def create_token(data: dict, expire_days = 0, expire_minutes = 15) -> str:
    if expire_days == 0 and expire_days <= 0:
        expire = datetime.now(timezone.utc) + timedelta(days=expire_minutes)
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=expire_days)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


def decode_token(token: str):
    auth_data = get_auth_data()
    try:
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
        return payload
    except JWTError:
        return None