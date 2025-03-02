from datetime import datetime
from src.dal.vacation_dao import VacationDao
from src.services import vacation_service
from src.models.vacation_dto import VacationDto
from src.dal.user_dao import UserDao
import datetime
from src.services import user_service
from src.models.user_dto import UserDto
from src.models.likes_dto import LikesDto
vacation_dao_instance = VacationDao()
vacations_service_instance = vacation_service.VacationService(vacation_dao_instance)







