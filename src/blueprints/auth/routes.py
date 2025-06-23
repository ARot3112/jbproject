from flask import Blueprint, render_template,request, redirect, url_for, flash, session,jsonify

from werkzeug.security import check_password_hash, generate_password_hash
from src.services.user_service import UserServices, UserDto, UserDao
from src.blueprints.auth.utils import login_required

auth_blueprint = Blueprint('auth', __name__, template_folder='src/templates', static_folder='src/static')
from flask import (
    Blueprint, render_template, request, jsonify,
    redirect, url_for, session, flash, abort
)
from werkzeug.security import check_password_hash


auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
    else:
        email = request.form.get('email')
        password = request.form.get('password')

    dao = UserDao()
    user = dao.get_password_by_email(email=email)
    if not user:
        if _wants_json():
            abort(400, description="User not found")
        flash("User not found")
        return redirect(url_for('auth.login'))

    if not check_password_hash(user['password'], password):
        if _wants_json():
            return jsonify({ "success": False, "message": "Incorrect password" }), 401
        flash("Incorrect password")
        return redirect(url_for('auth.login'))

    session['user_name']   = f"{user['first_name']} {user['last_name']}"
    session['user_id']     = user['id']
    session['user_role_id']= user['role_id']

    if _wants_json():
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

    return redirect(url_for('home'))


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')

    if request.is_json:
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
    else:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

    role_id = 1

    if not all([first_name, last_name, email, password]):
        if _wants_json():
            abort(400, description="All fields are required.")
        flash("All fields are required.")
        return redirect(url_for('auth.signup'))

    try:
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
        if _wants_json():
            return jsonify({ "success": True, "first_name": user_dto.first_name, "last_name": user_dto.last_name, "email": user_dto.email, "role_id": user_dto.role_id, "message": "User registered successfully" }), 201

        flash("SignUp Successfully")
        return redirect(url_for("auth.login"))

    except ValueError as e:
        flash(f"Signup Failed: {str(e)}")
        if _wants_json():
            return jsonify({ "success": False, "message": str(e) }), 400
        return redirect(url_for('auth.signup'))

    except Exception:
        flash("Something went wrong. Please try again.")
        if _wants_json():
            return jsonify({ "success": False, "message": "Something went wrong. Please try again." }), 500
        return redirect(url_for('auth.signup'))
@auth_blueprint.route('/logout')
@login_required
def logout():
    session.clear()
    if _wants_json():
        return jsonify({ "success": True, "message": "Logged out successfully" }), 200
    flash("Logged out successfully")
    return redirect(url_for('home'))





def _wants_json():
    return (
        request.is_json or
        request.accept_mimetypes['application/json'] >=
        request.accept_mimetypes['text/html']
    )
