from datetime import datetime
from src.dal.vacation_dao import VacationDao
from src.services import vacation_service
from src.models.vacation_dto import VacationDto
vacation_dao_instance = VacationDao()
vacation_service_instance = vacation_service.VacationService(vacation_dao_instance)
vacation_dto = VacationDto(country_id=9,vacation_description='This is some random try', arrival=datetime.strptime('2025-12-12', '%Y-%m-%d'),
    departure=datetime.strptime('2025-12-20' '%Y-%m-%d'),price=3000,file_name='jpg.something')
vacation_service_instance.insert_new_vacation_after_validation(vacation_dto)










