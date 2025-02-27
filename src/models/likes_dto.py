from dataclasses import dataclass

@dataclass
class LikesDto:
    user_id: int
    vacation_id: int