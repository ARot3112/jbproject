from src.dal import user_dao
from src.dal import country_dao
from src.dal import vacation_dao
from src.models.user_dto import UserDto
country_dao_instance = country_dao.CountryDao()
vacation_dao_instance = vacation_dao.VacationDao()
user_dao_instance = user_dao.UserDao()
user_dto = UserDto(first_name="LilKoKo",last_name="shalom",email="asdasd@gmail.com",password="123dasd",role_id=2)
user_dao_instance.insert_into_users(user_dto)










