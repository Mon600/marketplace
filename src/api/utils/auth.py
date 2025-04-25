import uuid
from datetime import datetime, timezone, timedelta

from jose import jwt, JWTError

from config import get_auth_data


def create_access_token(data: dict, ):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode = data.copy()
    to_encode.update({"exp": expire,})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


def create_refresh_token(data: dict) -> dict[str, str]:
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode = data.copy()
    token_id = str(uuid.uuid4())
    to_encode.update({
        "exp": expire,
        "jti": token_id,
        "type": "refresh"})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return {"token": encode_jwt, "token_id": token_id}


def decode_token(token: str):
    auth_data = get_auth_data()
    try:
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
        return payload
    except JWTError:
        return None