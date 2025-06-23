from flask import Blueprint, render_template, jsonify
from src.dal.database import db_conn
import psycopg.rows as pgrows
from src.blueprints.auth.utils import login_required
from flask import request, redirect, url_for, flash
from flask import session
from src.services.vacation_service import VacationDao, VacationDto, VacationService
from src.dal.likes_dao import LikesDao
from src.dal.user_dao import UserDao
from werkzeug.utils import secure_filename
import os
from src.dal.country_dao import CountryDao

vacations_blueprint = Blueprint(
    'vacations', __name__, template_folder='src/templates', static_folder='src/static')


@vacations_blueprint.route('/vacations_list', methods=['GET'])
@login_required
def list_vacations():
    user_dao = UserDao()
    user = user_dao.get_user_info_by_id(session['user_id'])
    
    vacation_dao = VacationDao()
    vacations = vacation_dao.get_all_vacations()
    
    likes_dao = LikesDao()
    for vacation in vacations:
        vacation['likes_count'] = likes_dao.get_likes_count(vacation['id'])
        
        user_like = likes_dao.get_likes_info_by_id(session['user_id'], vacation['id'])
        vacation['user_liked'] = len(user_like) > 0
    if _wants_json():
        return jsonify({"user": {
            "id": user['id'],
            "name": f"{user['first_name']} {user['last_name']}",
        },
        "vacations": vacations})
   
    
    return render_template('vacations/list_vacations.html', vacations=vacations, user=user)

@vacations_blueprint.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_vacation(id):
    vacation_dao = VacationDao()
    if request.method == 'GET':
        vacation = vacation_dao.get_vacation_info_by_id(id)
        if _wants_json():
            return jsonify(vacation),200
        return render_template('vacations/update_vacation.html', vacation=vacation)
    
    if request.method == 'POST':
        try:
            vacation_dao.update_vacation_info_by_id(id, 'country_id', request.form.get('country_id'))
            vacation_dao.update_vacation_info_by_id(id, 'vacation_description', request.form.get('vacation_description'))
            vacation_dao.update_vacation_info_by_id(id, 'arrival', request.form.get('arrival'))
            vacation_dao.update_vacation_info_by_id(id, 'departure', request.form.get('departure'))
            vacation_dao.update_vacation_info_by_id(id, 'price', request.form.get('price'))
            if 'image' in request.files and request.files['image'].filename != '':
                file = request.files['image']
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/media', filename))
                vacation_dao.update_vacation_info_by_id(id, 'file_name', filename)
            flash("Vacation updated successfully")
            if _wants_json():
                response = {
                    "success": True,
                    "vacation": {
                        "id": id,
                        "country_id": request.form.get('country_id'),
                        "vacation_description": request.form.get('vacation_description'),
                        "arrival": request.form.get('arrival'),
                        "departure": request.form.get('departure'),
                        "price": request.form.get('price'),
                        "file_name": filename
                    }
                }
                return jsonify(response), 200
            return redirect(url_for('vacations.list_vacations'))
            
        except Exception as e:
            flash(f"Error updating vacation: {str(e)}")
            if _wants_json():
                return jsonify({"success": False,"message": f"Error updating vacation: {str(e)}"}), 500
            return redirect(url_for('vacations.list_vacations'))

@vacations_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_vacation():
    country_dao = CountryDao()
    countries = country_dao.get_all_countries()
    if request.method == 'GET':
        if _wants_json():
            return jsonify(countries),200
        return render_template('vacations/create_vacation.html',countries=countries)
    if request.method == 'POST':
        try:
            file = request.files['image']
            filename = secure_filename(file.filename)
            basedir = os.path.abspath(os.path.dirname(__file__))
            upload_path = os.path.join(basedir, '..', 'static', 'media')  # עולה תיקייה אחת אם אתה ב־blueprint
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))
            vacation_dto = VacationDto(
                country_id=request.form.get('country_id'),
                vacation_description=request.form.get('vacation_description'),
                arrival=request.form.get('arrival'),
                departure=request.form.get('departure'),
                price=int(request.form.get('price')),
                file_name=filename
            )
            vacation_service = VacationService()
            vacation_service.register_new_vacation(vacation_dto)
            flash("Vacation created successfully")
            if _wants_json():
                response = {
                    "success": True,
                    "vacation": {
                        "country_id": request.form.get('country_id'),
                        "vacation_description": request.form.get('vacation_description'),
                        "arrival": request.form.get('arrival'),
                        "departure": request.form.get('departure'),
                        "price": request.form.get('price'),
                        "file_name": filename
                    }
                }
                return jsonify(response), 200
            return redirect(url_for('vacations.list_vacations'))
        except Exception as e:
            flash(f"Error creating vacation: {str(e)}")
            if _wants_json():
                return jsonify({"success": False,"message": f"Error creating vacation: {str(e)}"}), 500
            return redirect(url_for('vacations.list_vacations'))
        


@vacations_blueprint.route('/delete/<int:id>', methods=['GET', 'DELETE'])
@login_required
def delete_vacation(id):
    vacation_dao = VacationDao()
    if request.method == 'GET':
        vacation = vacation_dao.get_vacation_info_by_id(id)
        if _wants_json():
            return jsonify(vacation),200
        return render_template('vacations/delete_vacation.html', vacation=vacation)
    
    if request.method == 'DELETE':
        try:
            vacation_dao.delete_vacation_info_by_id(id)
            flash("Vacation deleted successfully")
            if _wants_json():
                return '',204
            return redirect(url_for('vacations.list_vacations'))
        except Exception as e:
            flash(f"Error deleting vacation: {str(e)}")
            if _wants_json():
                return jsonify({"success": False,"message": f"Error deleting vacation: {str(e)}"}), 500
            return redirect(url_for('vacations.list_vacations'))


@vacations_blueprint.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
def like_vacation(id):
    try:
        if 'user_id' not in session:
            flash("Please login first")
            if _wants_json():
                return jsonify({"success": False,"message": "Please login first"}), 401
            return redirect(url_for('auth.login'))
            
        likes_dao = LikesDao()
        user_id = session['user_id']
        
        existing_like = likes_dao.get_likes_info_by_id(user_id, id)
        
        if existing_like:
            likes_dao.delete_likes_info_by_id(user_id, id)
            flash("Like removed")
        else:
            likes_dao.insert_into_likes(user_id, id)
            flash("Vacation liked successfully")
            
        if _wants_json():
            response = {
                "success": True,
                "vacation": {
                    "id": id,
                    "user_liked": len(existing_like) == 0
                }
            }
            return jsonify(response), 200
            
        return redirect(url_for('vacations.list_vacations'))
        
    except Exception as e:
        db_conn.rollback()
        flash(f"Error with like: {str(e)}")
        if _wants_json():
            return jsonify({"success": False,"message": f"Error with like: {str(e)}"}), 500
        return redirect(url_for('vacations.list_vacations'))
    

def _wants_json():
    return (
        request.is_json or
        request.accept_mimetypes['application/json'] >=
        request.accept_mimetypes['text/html']
    )