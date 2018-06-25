from flask import jsonify
import copy
from bookrecord.helper import Helper
from bookrecord.models.models import db, Books, Users

def allBooks():
    """Return all books from the Database"""
    booksArr=[]
    response = copy.deepcopy(Helper.REQUEST_SUCCESS)
    try:
        books = Books.query.all()
        for book in books:
            booksArr.append(book.toDict())
        response['books']=booksArr
    except Exception as e:
        e_type , e_message =  Helper.parseException(e)
        response = copy.deepcopy(Helper.REQUEST_FAIL)
        response['error'] = e_message
    return jsonify(response)

def updateRating(request):
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

def removeBook(request):
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

def addBook(request):
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

def hasUpdateAccess(user_name, password):
    user = Users.query.filter_by(user_name=user_name,password=password).first()

    if user!=None and user.access==0:
        return True
    return False