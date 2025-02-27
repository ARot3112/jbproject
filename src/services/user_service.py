import re
from src.models.user_dto import UserDto
from src.dal.user_dao import UserDao
from src.models.likes_dto import LikesDto
from src.dal.likes_dao import LikesDao

class UserServices:
    def __init__(self):
        self.user_dao_instance = UserDao()
        self.likes_dao_instance = LikesDao()
    
    def validate_user_before_insert(self,user_dto):
        if not isinstance(user_dto,UserDto):
            raise TypeError("user_dto must be an instance of UserDto")
        
        if user_dto.role_id == 2:
            raise ValueError("Role_id cannot be 2, insert 1 instead")
        
        email_regex = r'^[A-Za-z0-9]+@[A-Za-z]+\.[A-Za-z]{2,}$'
        
        if not re.fullmatch(email_regex,user_dto.email):
            raise ValueError("This email is not valid")
        
        if len(user_dto.password) < 4:
            raise ValueError("Password must be at least 4 characters long")
        
        
        if self.user_dao_instance.check_if_email_exist(user_dto.email):
            raise ValueError("You cannot insert an existing email")
        
    def log_in_user(self,user_dto):
        if not user_dto.email or not user_dto.password:
            raise ValueError("You must enter password and email")
        email_regex = r'^[A-Za-z0-9]+@[A-Za-z]+\.[A-Za-z]{2,}$'
        
        if not re.fullmatch(email_regex,user_dto.email):
            raise ValueError("This email is not valid")
        if len(user_dto.password) < 4:
            raise ValueError("Password must be at least 4 characters long")
        
        
    def like_a_vacation(self,likes_dto):
        self.likes_dao_instance.insert_into_likes(likes_dto.user_id,likes_dto.vacation_id)
    
    def un_like_a_vacation(self,likes_dto):
        self.likes_dao_instance.delete_likes_info_by_id(likes_dto.user_id,likes_dto.vacation_id)
        


        


    
