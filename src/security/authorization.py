from datetime import datetime
from functools import wraps
import jwt
from flask import jsonify, request
import logging

from security.blacklist_cache import BlackListCache
from configuration.models import JwtConfig
from .models import AccessType, AccessHierarchy

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def authorize(cache: BlackListCache, required_access: AccessType, config: JwtConfig):
    """
   Authorization decorator for Flask routes.

   This decorator checks the authorization of the incoming request based on the provided JWT token.
   It verifies the token, checks for expiration, and compares the user's access rights with the required access.

   Args:
       cache (BlackListCache): Cache instance for blacklisting users.
       required_access (AccessType): The required access level for the decorated route.
       config (JwtConfig): Configuration for JWT token validation.

   Returns:
       function: Decorated function.

   Raises:
       jwt.exceptions.ExpiredSignatureError: If the JWT token has expired.
       jwt.exceptions.InvalidTokenError: If the JWT token is invalid.
       KeyError: If 'email', 'exp', or 'access' is not present in the decoded token.
   """

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            logger.info("Checking authorization")

            auth_header = request.headers.get("Authorization")

            if not auth_header:
                logger.warning("Authorization header missing")
                return jsonify({"error": "Authorization header missing"}), 401

            token = auth_header.split(" ")[1]

            try:
                decoded_token = jwt.decode(token, config.encryption_key, algorithms=config.algorithm)
            except jwt.exceptions.ExpiredSignatureError:
                logger.warning("Token has expired")
                return jsonify({"error": "Token has expired"}), 401
            except jwt.exceptions.InvalidTokenError:
                logger.warning("Invalid token")
                return jsonify({"error": "Invalid token"}), 401

            if "email" not in decoded_token:
                logger.warning("Email not found in token")
                return jsonify({"error": "Email not found in token"}), 401

            if "exp" not in decoded_token:
                logger.warning("Expiration time not found in token")
                return jsonify({"error": "Expiration time not found in token"}), 401

            email = decoded_token["email"]
            exp = decoded_token["exp"]
            access: str = decoded_token["access"]

            if datetime.fromtimestamp(exp) < datetime.utcnow():
                logger.warning("Token has expired")
                return jsonify({"error": "Token has expired"}), 401

            if cache.get(email):
                logger.warning("Email is blacklisted")
                return jsonify({"error": "User is blacklisted"}), 401

            if required_access not in AccessHierarchy[access].value:
                logger.warning(f"Insufficient access: {access} < {required_access.to_string()}")
                return jsonify({"error": "Insufficient access rights"}), 403

            logger.info(f"Authorization successful: {access} >= {required_access.to_string()}")
            return f(*args, **kwargs)

        return decorated

    return decorator
