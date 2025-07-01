# API.py
from flask import Blueprint, request, jsonify, abort, session
from werkzeug.security import check_password_hash, generate_password_hash
from src.services.user_service import UserServices, UserDto, UserDao
from src.blueprints.auth.utils import login_required

auth_api = Blueprint('auth_api', __name__, url_prefix='/api/auth')


@auth_api.route('/login', methods=['POST'])
def login():
    """
    Logs in a user with the given email and password.
    Args:
        email (str): The user's email.
        password (str): The user's password.
    Returns:
        A JSON response containing the user's information.
    Raises:
        400: User not found or incorrect password.
    """
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        abort(400, description="Missing email or password")

    dao = UserDao()
    user = dao.get_password_by_email(email=email)
    if not user:
        abort(400, description="User not found")
    if not check_password_hash(user['password'], password):
        abort(400, description="Incorrect password")
    
    session['user_name'] = f"{user['first_name']} {user['last_name']}"
    session['user_id'] = user['id']
    session['user_role_id'] = user['role_id']


    return jsonify({
        "success": True,
        "user": {
            "id": user['id'],
            "email": user['email'],
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "role_id": user['role_id']
        }
    }), 200
@auth_api.route('/signup', methods=['POST'])
def signup():
    """
    Registers a new user with the given details.
    Args:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address.
        password (str): The user's password.
    Returns:
        JSON response indicating the success of the operation
        and the user's details on successful registration.
    Raises:
        400: If any required field is missing.
    """

    data = request.get_json() or {}
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    role_id = 1

    if not all([first_name, last_name, email, password]):
        abort(400, description="All fields are required.")

    hashed_password = generate_password_hash(password)
    user_dto = UserDto(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password,
        role_id=role_id
    )
    service = UserServices()
    service.register_new_user(user_dto)
    return jsonify({
        "success": True,
        "first_name": user_dto.first_name,
        "last_name": user_dto.last_name,
        "email": user_dto.email,
        "role_id": user_dto.role_id,
        "message": "User registered successfully"
    }), 201
@auth_api.route('/logout', methods=['GET','DELETE'])
@login_required
def logout():
    
    
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully"}), 200


