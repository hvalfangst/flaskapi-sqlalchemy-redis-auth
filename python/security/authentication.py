import sys
import traceback

import bcrypt


def authenticate(user, password: str) -> tuple[bool, str | None]:
    """
    Authenticate a user based on provided email and password.

    Args:
        user
        password (str): Password provided for authentication.

    Returns:
        tuple: A tuple containing a boolean indicating authentication success and the user's access level.
    """
    try:
        if not user:
            return False, None

        stored_password = user.password.encode('utf-8')
        request_password = password.encode('utf-8')
        return bcrypt.checkpw(request_password, stored_password), user.access
    except Exception as e:
        print(f"Error occurred: {str(e)}\n{traceback.format_exc()}", file=sys.stderr)
        return False, None