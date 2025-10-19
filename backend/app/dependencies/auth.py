# app/dependencies/auth.py
from fastapi import Header
from app.utils.jwt import decode_access_token

def get_current_user(info):
    request = info.context["request"]
    authorization = request.headers.get("authorization")
    if not authorization:
        raise Exception("Authorization header missing")
    if not authorization.startswith("Bearer "):
        raise Exception("Invalid token format")
    token = authorization.split(" ")[1]
    try:
        user = decode_access_token(token)
        return user
    except Exception as e:
        raise Exception(f"Unauthorized: {str(e)}")

