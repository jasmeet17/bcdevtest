from flask import jsonify
import copy
from bookrecord.helper import Helper
from bookrecord.data.models import db, Users

def addUserController(request):
    """Add a user in the Database"""
    user_name = request.json.get('user_name')
    password = request.json.get('password')
    access = request.json.get('access')
    response = copy.deepcopy(Helper.REQUEST_FAIL)

    if user_name is None or password is None:
        response['error']="Please enter all details"
        return jsonify(response)
    else:
        response = copy.deepcopy(Helper.REQUEST_SUCCESS)
        new_user = Users(user_name=user_name, password=password, access=access)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:            
            e_type , e_message =  Helper.parseException(e)
            response = copy.deepcopy(Helper.REQUEST_FAIL)
            response['error'] = e_message
    return jsonify(response)