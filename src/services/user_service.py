import re
from src.models.user_dto import UserDto
from src.dal.user_dao import UserDao
from src.models.likes_dto import LikesDto
from src.dal.likes_dao import LikesDao


class UserServices:
    def __init__(self) -> None:
        """
        Initializes the user services and connects the UserDAO and LikesDAO layers.
        """
        self.user_dao: UserDao = UserDao()
        self.likes_dao: LikesDao = LikesDao()

    def validate_user_before_insert(self, user_dto: UserDto) -> None:
        """
        Validates the user data before inserting it into the database.

        :param user_dto: UserDto object containing the user's data.
        :raises TypeError: If user_dto is not an instance of UserDto.
        :raises ValueError: If role_id is 2, email format is invalid, password is too short,
                           or if the email already exists in the system.
        """
        if not isinstance(user_dto, UserDto):
            raise TypeError("UserDto type expected for user_dto.")

        if user_dto.role_id == 2:
            raise ValueError("Invalid role_id: 2 is not allowed. Use role_id 1 instead.")

        email_regex: str = r'^[A-Za-z0-9]+@[A-Za-z]+\.[A-Za-z]{2,}$'
        if not re.fullmatch(email_regex, user_dto.email):
            raise ValueError("Invalid email format provided.")

        if len(user_dto.password) < 4:
            raise ValueError("Password is too short; it must be at least 4 characters long.")

        if self.user_dao.check_if_email_exist(user_dto.email):
            raise ValueError("The email provided already exists in the system.")

    def register_new_user(self, user_dto: UserDto) -> None:
        """
        Registers a new user by validating and then inserting the user's data into the database.

        :param user_dto: UserDto object containing the user's registration data.
        """
        self.validate_user_before_insert(user_dto)
        self.user_dao.insert_into_users(user_dto)

    def log_in_user(self, user_dto: UserDto) -> None:
        """
        Validates user credentials during login.

        :param user_dto: UserDto object containing the user's email and password.
        :raises ValueError: If email or password is missing, if email format is invalid,
                            or if the password is too short.
        """
        if not user_dto.email or not user_dto.password:
            raise ValueError("Both email and password must be provided for login.")

        email_regex: str = r'^[A-Za-z0-9]+@[A-Za-z]+\.[A-Za-z]{2,}$'
        if not re.fullmatch(email_regex, user_dto.email):
            raise ValueError("Invalid email format provided.")

        if len(user_dto.password) < 4:
            raise ValueError("Password is too short; it must be at least 4 characters long.")

    def like_a_vacation(self, likes_dto: LikesDto) -> None:
        """
        Allows a user to like a specific vacation by inserting a like record into the database.

        :param likes_dto: LikesDto object containing the like data (user_id and vacation_id).
        :raises TypeError: If either user_id or vacation_id is not an integer.
        """
        if not isinstance(likes_dto.user_id, int) or not isinstance(likes_dto.vacation_id, int):
            raise TypeError("Both user_id and vacation_id must be integers.")
        self.likes_dao.insert_into_likes(likes_dto.user_id, likes_dto.vacation_id)

    def un_like_a_vacation(self, likes_dto: LikesDto) -> None:
        """
        Allows a user to remove a like from a specific vacation by deleting the like record from the database.

        :param likes_dto: LikesDto object containing the like data (user_id and vacation_id).
        :raises TypeError: If either user_id or vacation_id is not an integer.
        """
        likes_dto.vacation_id = int(likes_dto.vacation_id)
        if not isinstance(likes_dto.user_id, int) or not isinstance(likes_dto.vacation_id, int):
            raise TypeError("Both user_id and vacation_id must be integers.")
        self.likes_dao.delete_likes_info_by_id(likes_dto.user_id, likes_dto.vacation_id)

