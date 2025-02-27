from dataclasses import dataclass

@dataclass
class VacationDto:
    country_id: int
    vacation_description: str
    arrival: str
    departure: str
    price: int
    file_name: str