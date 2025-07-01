from flask import Blueprint, render_template,request, redirect, url_for, flash, session
from src.dal.database import db_conn
from src.blueprints.auth.utils import login_required
from src.services.vacation_service import VacationDao, VacationDto, VacationService
from src.dal.likes_dao import LikesDao
from src.dal.user_dao import UserDao
from src.dal.country_dao import CountryDao
from werkzeug.utils import secure_filename
import os
from flask import current_app

vacations_ui = Blueprint(
    'vacations_ui', __name__, template_folder='src/templates', static_folder='src/static',url_prefix='/vacations')


@vacations_ui.route('/vacations_list', methods=['GET'])
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
   
    
    return render_template('vacations/list_vacations.html', vacations=vacations, user=user)

@vacations_ui.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_vacation(id):
    dao = VacationDao()

    if request.method == 'GET':
        vacation = dao.get_vacation_info_by_id(id)
        return render_template('vacations/update_vacation.html', vacation=vacation)
    try:
        dao.update_vacation_info_by_id(id, 'country_id',          request.form['country_id'])
        dao.update_vacation_info_by_id(id, 'vacation_description', request.form['vacation_description'])
        dao.update_vacation_info_by_id(id, 'arrival',              request.form['arrival'])
        dao.update_vacation_info_by_id(id, 'departure',            request.form['departure'])
        dao.update_vacation_info_by_id(id, 'price',                request.form['price'])

        uploaded = request.files.get('image')
        if uploaded and uploaded.filename:
            filename = secure_filename(uploaded.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            uploaded.save(file_path)
            dao.update_vacation_info_by_id(id, 'file_name', filename)

        flash("Vacation updated successfully")
        return redirect(url_for('vacations_ui.list_vacations'))

    except Exception as e:
        flash(f"Error updating vacation: {e}")
        return redirect(url_for('vacations_ui.list_vacations'))


@vacations_ui.route('/create', methods=['GET', 'POST'])
@login_required
def create_vacation():
    country_dao = CountryDao()
    countries = country_dao.get_all_countries()

    if request.method == 'GET':
        return render_template('vacations/create_vacation.html', countries=countries)

    try:
        country_id  = request.form['country_id']
        description = request.form['vacation_description']
        arrival     = request.form['arrival']
        departure   = request.form['departure']
        price       = int(request.form['price'])

        uploaded = request.files.get('image')
        filename = None
        if uploaded and uploaded.filename:
            filename = secure_filename(uploaded.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            uploaded.save(file_path)

        vacation_dto = VacationDto(
            country_id=country_id,
            vacation_description=description,
            arrival=arrival,
            departure=departure,
            price=price,
            file_name=filename
        )
        VacationService().register_new_vacation(vacation_dto)

        flash("Vacation created successfully")
        return redirect(url_for('vacations_ui.list_vacations'))

    except Exception as e:
        flash(f"Error creating vacation: {e}")
        return redirect(url_for('vacations_ui.list_vacations'))

@vacations_ui.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_vacation(id):
    vacation_dao = VacationDao()
    if request.method == 'GET':
        vacation = vacation_dao.get_vacation_info_by_id(id)
        return render_template('vacations/delete_vacation.html', vacation=vacation)
    
    if request.method == 'POST':
        try:
            vacation_dao.delete_vacation_info_by_id(id)
            flash("Vacation deleted successfully")
            return redirect(url_for('vacations_ui.list_vacations'))
        except Exception as e:
            flash(f"Error deleting vacation: {str(e)}")
            return redirect(url_for('vacations_ui.list_vacations'))


@vacations_ui.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
def like_vacation(id):
    try:
            
        likes_dao = LikesDao()
        user_id = session['user_id']
        
        existing_like = likes_dao.get_likes_info_by_id(user_id, id)
        
        if existing_like:
            likes_dao.delete_likes_info_by_id(user_id, id)
            flash("Like removed")
        else:
            likes_dao.insert_into_likes(user_id, id)
            flash("Vacation liked successfully")
            
            
        return redirect(url_for('vacations_ui.list_vacations')), 302
        
    except Exception as e:
        db_conn.rollback()
        flash(f"Error with like: {str(e)}")
        return redirect(url_for('vacations_ui.list_vacations'))
    
