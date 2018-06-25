from flask import jsonify
import copy
from bookrecord.helper import Helper
from bookrecord.data.models import db, Books, Users

def removeBookController(request):
    """Remove book form the Batabase, If user has Access"""
    response = copy.deepcopy(Helper.REQUEST_FAIL)
    user_name = request.json.get('user_name')
    password = request.json.get('password')

    if user_name is None or password is None:
        response['error']="User detail incorrect"
        return jsonify(response)
    elif not hasAddDeleteAccess(user_name, password):
        response['error']="User doesn't have Delete access"
        return jsonify(response)

    response = copy.deepcopy(Helper.REQUEST_SUCCESS)

    isbn = request.json.get('isbn')
    book = Books.query.filter_by(isbn=isbn).first()

    if book==None:
        response = copy.deepcopy(Helper.REQUEST_FAIL)
        response['error']="No such book exists"
        return jsonify(response)
    else:
        db.session.delete(book)
        db.session.commit()
    return jsonify(response)

def hasAddDeleteAccess(user_name, password):
    user = Users.query.filter_by(user_name=user_name,password=password).first()

    if user!=None and user.access==1:
        return True
    return False