from flask import Blueprint, render_template,request, redirect, url_for, flash, session,jsonify

# UI.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from src.services.user_service import UserServices, UserDto, UserDao
from src.blueprints.auth.utils import login_required

auth_ui = Blueprint('auth_ui', __name__, url_prefix='/auth', template_folder='templates', static_folder='static')


@auth_ui.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    email = request.form.get('email')
    password = request.form.get('password')

    dao = UserDao()
    user = dao.get_password_by_email(email=email)
    if not user:
        flash("User not found")
        return redirect(url_for('auth_ui.login')), 400

    if not check_password_hash(user['password'], password):
        flash("Incorrect password")
        return redirect(url_for('auth_ui.login')), 400

    session['user_name']   = f"{user['first_name']} {user['last_name']}"
    session['user_id']     = user['id']
    session['user_role_id']= user['role_id']

    return redirect(url_for('home')), 200


@auth_ui.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    role_id = 1

    if not all([first_name, last_name, email, password]):
        flash("All fields are required.")
        return redirect(url_for('auth_ui.signup')), 400

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
    
        flash("SignUp Successfully")
        return redirect(url_for("auth_ui.login")), 200

    except ValueError as e:
        flash(f"Signup Failed: {str(e)}")
        return redirect(url_for('auth_ui.signup')), 400

    except Exception:
        flash("Something went wrong. Please try again.")
        return redirect(url_for('auth_ui.signup')), 500
@auth_ui.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for('home')), 200




