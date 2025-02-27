from dataclasses import dataclass
from enum import Enum

class RoleEnum(Enum):
    USER = "user"
    ADMIN = "admin"

@dataclass
class RoleDTO:
    name: RoleEnum