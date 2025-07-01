from tests.runner import test_all
from src.models.user_dto import UserDto
from src.dal.user_dao import UserDao
# user = UserDto("Afek","Rot","afekrotstain14@gmail.com",'12345678',2)
if __name__ == "__main__":
    # user_dao = UserDao()
    # user_dao.insert_into_users(user)
    test_all()




