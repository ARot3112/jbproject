from flask import Flask, render_template, request, session,jsonify
from werkzeug.security import generate_password_hash
from src.blueprints.auth.api import auth_api
from src.blueprints.auth.ui import auth_ui
from src.blueprints.vacations.api import vacations_api
from src.blueprints.vacations.ui import vacations_ui

import os

app = Flask(__name__, static_folder="src/static",
            template_folder="src/templates")
app.secret_key = "really_secret_key"
basedir = os.path.abspath(os.path.dirname(__file__))
upload_path = os.path.join(basedir, 'src', 'static', 'media')
os.makedirs(upload_path, exist_ok=True)           
app.config['UPLOAD_FOLDER'] = upload_path    
app.register_blueprint(auth_ui, url_prefix='/auth')
app.register_blueprint(auth_api, url_prefix='/api/auth')
app.register_blueprint(vacations_ui, url_prefix='/vacations')
app.register_blueprint(vacations_api, url_prefix='/api/vacations')


@app.errorhandler(400)
def handle_bad_request(e):
    if request.path.startswith('/api/'):
        return jsonify(success=False, message=str(e)), 400
    return render_template('errors/400.html', error=e), 400

@app.errorhandler(401)
def handle_unauthorized(e):
    if request.path.startswith('/api/'):
        return jsonify(success=False, message=str(e)), 401
    return render_template('errors/401.html', error=e), 401

@app.errorhandler(404)
def handle_not_found(e):
    if request.path.startswith('/api/'):
        return jsonify(success=False, message="Resource not found"), 404
    return render_template('errors/404.html', error=e), 404

@app.errorhandler(500)
def handle_server_error(e):
    if request.path.startswith('/api/'):
        return jsonify(success=False, message="Internal Server Error"), 500
    return render_template('errors/500.html', error=e), 500

@app.route("/")
def home():
    return render_template('index.html')

@app.context_processor
def inject_user_role():
    return {
        'user_role_id': session.get('role_id'),
        'user': session.get('user') 
    }
# from src.models.user_dto import UserDto
# from src.dal.user_dao import UserDao
# password = '12345678'
# user = UserDto("Afek","Rot","afekrotstain14@gmail.com",generate_password_hash(password),2)
# user_dao = UserDao()
# user_dao.delete_user_info_by_id(1)
# user_dao.insert_into_users(user)
# app.run(debug=False)