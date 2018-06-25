from flask import jsonify
import copy
from bookrecord.helper import Helper
from bookrecord.data.models import db, Books, Users

def updateRatingController(request):
    """Update rating of a book"""
    response = copy.deepcopy(Helper.REQUEST_FAIL)
    user_name = request.json.get('user_name')
    password = request.json.get('password')

    if user_name is None or password is None:
        response['error']="User detail incorrect"
        return jsonify(response)
    elif not hasUpdateAccess(user_name, password):
        response['error']="User doesn't have Rating access"
        return jsonify(response)

    isbn = request.json.get('isbn')
    newRating = request.json.get('rating')
    book = Books.query.filter_by(isbn=isbn).first()

    if book==None:
        response['error']="No such book exists"
    elif newRating==None or newRating<0 or newRating>10:
        response['error']="Please Rate between 0-10"
    else:
        rating = book.rating
        rating = rating + newRating
        book.rating = rating/2
        db.session.commit()
        response = copy.deepcopy(Helper.REQUEST_SUCCESS)
    return jsonify(response)

def hasUpdateAccess(user_name, password):
    user = Users.query.filter_by(user_name=user_name,password=password).first()

    if user!=None and user.access==0:
        return True
    return False