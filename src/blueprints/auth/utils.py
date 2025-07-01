from functools import wraps
from flask import session, redirect, url_for, flash
from flask import jsonify,request, abort


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in session:
            if _wants_json():
                return jsonify({"error": "Unauthorized access"}), 401
            flash("Please log in or sign up to access this page.")
            return redirect(url_for('auth.ui.login'))
        return f(*args, **kwargs)
    return decorated_function

def _wants_json():
    return (
        request.is_json or
        request.accept_mimetypes['application/json'] >=
        request.accept_mimetypes['text/html']
    )