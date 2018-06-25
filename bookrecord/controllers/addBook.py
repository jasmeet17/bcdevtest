from flask import jsonify
import copy
from bookrecord.helper import Helper
from bookrecord.data.models import db, Books, Users

def addBookController(request):
    """Add a Book in the Database, if User has Access"""
    response = copy.deepcopy(Helper.REQUEST_FAIL)
    user_name = request.json.get('user_name')
    password = request.json.get('password')

    if user_name is None and password is None:
        response['error']="User detail incorrect"
        return jsonify(response)
    elif not hasAddDeleteAccess(user_name, password):
        response['error']="User doesn't have add access"
        return jsonify(response)

    isbn = request.json.get('isbn')
    title = request.json.get('title')
    author = request.json.get('author')
    genre = request.json.get('genre')
    price = request.json.get('price')
    print isbn, title
    book = Books(isbn=isbn, title=title, author=author, genre=genre, price=price)
    
    try:
        db.session.add(book)
        db.session.commit()
        response = copy.deepcopy(Helper.REQUEST_SUCCESS)
    except Exception as e:
        e_type , e_message =  Helper.parseException(e)
        response = copy.deepcopy(Helper.REQUEST_FAIL)
        response['error'] = e_message
        
    return jsonify(response)

def hasAddDeleteAccess(user_name, password):
    user = Users.query.filter_by(user_name=user_name,password=password).first()

    if user!=None and user.access==1:
        return True
    return False