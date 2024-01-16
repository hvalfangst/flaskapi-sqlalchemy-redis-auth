import sys
from datetime import datetime, timedelta

import bcrypt
import jwt
from flask import jsonify, request

from python.config.jwt.module import JwtConfig
from python.config.redis.module import RedisCacheConfig
from python.messages.module import UserMessages
from python.repository.redis.module import RedisUserRepository
from python.util.module import UserPayloadConverter

redis_config = RedisCacheConfig(host="localhost", port=6379, password="", key_prefix="users")
cache = RedisUserRepository(config=redis_config)
jwt_config = JwtConfig(encryption_key="MisterPastor77", algorithm="HS256", expiration=5)


def create_user_handler():
    request_json = request.get_json()

    if not all(field in request_json for field in
               ['email', 'password', 'access']):
        return jsonify({"error": UserMessages.FIELD_REQUIRED}), 400

    email = request_json['email']

    if cache.email_exists(email):
        return jsonify({"error": UserMessages.USER_EXISTS.format(email=email)}), 409

    try:
        user_data = UserPayloadConverter.to_user_payload(request_json)
        cache.create(key=email, user=user_data)
        return jsonify({"message": UserMessages.SUCCESSFUL_CREATION})
    except Exception as e:
        error_message = UserMessages.ERROR_OCCURRED.format(error=str(e))
        print(error_message, file=sys.stderr)
        return jsonify({"error": error_message})


def list_users_handler():
    try:
        users = cache.list()
        return jsonify({"users": users})
    except Exception as e:
        error_message = UserMessages.ERROR_OCCURRED.format(error=str(e))
        print(error_message, file=sys.stderr)
        return jsonify({"error": error_message})


def get_user_handler(email: str):
    try:
        user = cache.get(key=email)
        return jsonify({"user": user})
    except KeyError:
        return jsonify({"error": UserMessages.USER_NOT_FOUND.format(key=key)}), 404
    except Exception as e:
        error_message = UserMessages.ERROR_OCCURRED.format(error=str(e))
        print(error_message, file=sys.stderr)
        return jsonify({"error": error_message})


def delete_user_handler(email: str):
    try:
        cache.delete(key=email)
        return jsonify({"message": UserMessages.USER_DELETED})
    except KeyError:
        return jsonify({"error": UserMessages.USER_NOT_FOUND.format(key=email)}), 404
    except Exception as e:
        error_message = UserMessages.ERROR_OCCURRED.format(error=str(e))
        print(error_message, file=sys.stderr)
        return jsonify({"error": error_message})


def login_user_handler():
    request_json = request.get_json()
    email = request_json.get('email')
    password = request_json.get('password')

    if not (email and password):
        return jsonify({"error": UserMessages.MISSING_CREDENTIALS}), 400

    if authenticate(email, password):
        token = generate_jwt_token(email)
        return jsonify({"token": token})
    else:
        return jsonify({"error": UserMessages.USER_UNAUTHORIZED}), 401


def authenticate(email: str, password: str):
    if not cache.email_exists(email):
        return False

    data = cache.get(email)
    hashed_password_bytes = data.get("password").encode('utf-8')
    provided_password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(provided_password_bytes, hashed_password_bytes)


def generate_jwt_token(config: JwtConfig, email: str):
    expiration_time = datetime.utcnow() + timedelta(minutes=config.expiration)
    payload = {
        "email": email,
        "exp": expiration_time
    }
    token = jwt.encode(payload, config.encryption_key, algorithm=config.algorithm)
    return token
