from typing import Any, Dict


class UserPayload:
    def __init__(self, email: str, password: str, access: str) -> None:
        self.email = email
        self.password = password
        self.access = access

    def to_dict(self) -> Dict[str, Any]:
        return {
            "email": self.email,
            "password": self.password,
            "access": self.access
        }


class UserPayloadConverter:
    @staticmethod
    def to_user_payload(request_json: Any) -> UserPayload:
        email = request_json.get('email')
        password = request_json.get('password')
        access = request_json.get('access')
        return UserPayload(email=email, password=password, access=access)
