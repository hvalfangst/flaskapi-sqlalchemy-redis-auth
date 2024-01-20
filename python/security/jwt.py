import sys
import traceback
from datetime import datetime, timedelta
import jwt
from pydantic import EmailStr
from configuration.models import JwtConfig
from users.models import Claims


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