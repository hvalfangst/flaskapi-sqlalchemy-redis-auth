from .models import Claims
from .repository import UsersRepository
from common.configs import JwtConfig
from pydantic import EmailStr
import sys
import traceback
from datetime import datetime, timedelta

import bcrypt
import jwt


def authenticate(db: UsersRepository, email: EmailStr, password: str) -> tuple[bool, str | None]:
    """
    Authenticate a user based on provided email and password.

    Args:
        db (UsersRepository): Database repository for user data.
        email (EmailStr): Email of the user.
        password (str): Password provided for authentication.

    Returns:
        tuple: A tuple containing a boolean indicating authentication success and the user's access level.
    """
    try:
        user = db.get_by_email(email)

        if not user:
            return False, None

        stored_password = user.password.encode('utf-8')
        request_password = password.encode('utf-8')
        return bcrypt.checkpw(request_password, stored_password), user.access
    except Exception as e:
        print(f"Error occurred: {str(e)}\n{traceback.format_exc()}", file=sys.stderr)
        return False, None


def generate_jwt_token(config: JwtConfig, email: EmailStr, access: str) -> str | None:
    """
   Generate a JWT token for a user.

   Args:
       config (JwtConfig): JWT configuration.
       email (EmailStr): Email of the user.
       access (str): Access level of the user.

   Returns:
       str | None: JWT token if successful, None otherwise.
   """
    try:
        expiration_time = datetime.utcnow() + timedelta(minutes=config.expiration)
        claims = Claims(email, access, expiration_time)
        token = jwt.encode(claims.to_dict(), config.encryption_key, algorithm=config.algorithm)
        return token
    except Exception as e:
        print(f"Error occurred: {str(e)}\n{traceback.format_exc()}", file=sys.stderr)
        return None
