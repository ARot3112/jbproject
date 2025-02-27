from dataclasses import dataclass

@dataclass
class UserDto:
    first_name: str
    last_name: str
    email: str
    password: str
    role_id: int
