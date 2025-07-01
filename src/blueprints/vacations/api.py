from flask import Blueprint,  jsonify,request, abort,   session
from src.dal.database import db_conn
from src.blueprints.auth.utils import login_required
from src.services.vacation_service import VacationDao, VacationDto, VacationService
from src.dal.likes_dao import LikesDao
from src.dal.user_dao import UserDao
from src.dal.country_dao import CountryDao
from werkzeug.utils import secure_filename
from flask import current_app
import os

vacations_api = Blueprint(
    'vacations_api', __name__, template_folder='src/templates', static_folder='src/static', url_prefix='/api/vacations')


@vacations_api.route('/vacations_list', methods=['GET'])
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
    return jsonify({"user": {
        "id": user['id'],
        "name": f"{user['first_name']} {user['last_name']}",
    },
    "vacations": vacations})
   
    
@vacations_api.route('/update/<int:id>', methods=['PUT'])
@login_required  
def update_vacation(id):
    existing = VacationDao().get_vacation_info_by_id(id)
    filename = existing.get('file_name')
    
    data = request.json
    country_id = data['country_id']
    description = data['vacation_description']
    arrival = data['arrival']
    departure = data['departure']
    price = int(data['price'])

    dao = VacationDao()
    dao.update_vacation_info_by_id(id, 'country_id', country_id)
    dao.update_vacation_info_by_id(id, 'vacation_description', description)
    dao.update_vacation_info_by_id(id, 'arrival', arrival)
    dao.update_vacation_info_by_id(id, 'departure', departure)
    dao.update_vacation_info_by_id(id, 'price', price)

    return jsonify({
        "success": True,
        "vacation": {
            "id": id,
            "country_id": country_id,
            "vacation_description": description,
            "arrival": arrival,
            "departure": departure,
            "price": price,
            "file_name": filename
        }
    }), 200
    
@vacations_api.route('/create', methods=['POST'])
@login_required  
def create_vacation():
    try:
        data = request.json
        country_id = data['country_id']
        description = data['vacation_description']
        arrival = data['arrival']
        departure = data['departure']
        price = int(data['price'])

        vacation_dto = VacationDto(
            country_id=country_id,
            vacation_description=description,
            arrival=arrival,
            departure=departure,
            price=price,
            file_name=None  
        )
        VacationService().register_new_vacation(vacation_dto)

        return jsonify({
            "success": True,
            "vacation": vacation_dto.__dict__
        }), 201
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
        


@vacations_api.route('/delete/<int:id>', methods=[ 'DELETE'])
@login_required
def delete_vacation(id):
    vacation_dao = VacationDao()    
    vacation_dao.delete_vacation_info_by_id(id)
    return jsonify({"success": True, "message": "Vacation deleted successfully"}), 200
           

@vacations_api.route('/like/<int:id>', methods=[ 'POST'])
@login_required
def like_vacation(id):
    if 'user_id' not in session:
        abort(401, description="Unauthorized: User not logged in")
    
    likes_dao = LikesDao()
    user_id = session['user_id']
    
    existing_like = likes_dao.get_likes_info_by_id(user_id, id)
    
    if existing_like:
        likes_dao.delete_likes_info_by_id(user_id, id)
        user_liked = False
    else:
        likes_dao.insert_into_likes(user_id, id)
        user_liked = True
    
    response = {
        "success": True,
        "vacation": {
            "id": id,
            "user_liked": user_liked  
        }
    }
    return jsonify(response), 200