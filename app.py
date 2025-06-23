from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint

from src.dal.database import db_conn
from src.blueprints.auth.routes import auth_blueprint
from src.blueprints.vacations.routes import vacations_blueprint


app = Flask(__name__, static_folder="src/static",
            template_folder="src/templates")
app.secret_key = "really_secret_key"
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(vacations_blueprint, url_prefix='/vacations')


@app.route("/")
def home():
    return render_template('index.html')

@app.context_processor
def inject_user_role():
    return {
        'user_role_id': session.get('role_id'),
        'user': session.get('user') 
    }

