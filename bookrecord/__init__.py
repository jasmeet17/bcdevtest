from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask_sqlalchemy import Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, inspect
import re
import os
import json
from helper import Helper
from bookrecord.data.models import db, Users, Books
from bookrecord.utils import get_instance_folder_path


END_POINT = os.environ['END_POINT']
USER_NAME = os.environ['USER_NAME']
PASSWORD = os.environ['PASSWORD']


REQUEST_SUCCESS = {'success': True}
REQUEST_FAIL = {'success': False, 'error':''}

app = Flask(__name__,instance_path=get_instance_folder_path(),
            instance_relative_config=True)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+ USER_NAME + ':' + PASSWORD + '@' + END_POINT



def hasAddDeleteAccess(user_name, password):
    user = Users.query.filter_by(user_name=user_name,password=password).first()

    if user!=None and user.access==1:
        return True
    return False

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request - 400'}), 400)

@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify(REQUEST_SUCCESS)

@app.route("/books", methods=["GET", "POST"])
def books():
    books = Books.query.all()
    booksArr=[]

    for book in books:
        booksArr.append(book.toDict())
    return jsonify(booksArr)

@app.route("/add_user", methods=["POST"])
def addUser():
    user_name = request.json.get('user_name')
    password = request.json.get('password')
    access = request.json.get('access')
    response = REQUEST_FAIL

    if user_name is None or password is None:
        response['error']="Please enter all details"
        return jsonify(response)
    else:
        response = REQUEST_SUCCESS
        new_user = Users(user_name, password, access)
        db.session.add(new_user)
        db.session.commit()
    return jsonify(response)


@app.route("/add_book", methods=["POST"])
def addBook():
    response = REQUEST_FAIL
    user_name = request.json.get('user_name')
    password = request.json.get('password')

    if user_name is None and password is None:
        response['error']="User detail incorrect"
        return jsonify(response)
    elif not hasAddDeleteAccess(user_name, password):
        response['error']="User doesn't have add access"
        return jsonify(response)

    response = REQUEST_SUCCESS

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
    except Exception as e:
        e_type , e_message =  Helper.parseException(e)
        response = REQUEST_FAIL
        response['error'] = e_message
        
    return jsonify(response)

@app.route("/remove_book", methods=["DELETE"])
def remove():
    response = REQUEST_FAIL

    user_name = request.json.get('user_name')
    password = request.json.get('password')

    if user_name is None and password is None:
        response['error']="User detail incorrect"
        return jsonify(response)
    elif not hasAddDeleteAccess(user_name, password):
        response['error']="User doesn't have Delete access"
        return jsonify(response)

    response = REQUEST_SUCCESS

    isbn = request.json.get('isbn')
    book = Books.query.filter_by(isbn=isbn).first()

    if book==None:
        response = REQUEST_FAIL
        response['error']="No such book exists"
        return jsonify(response)
    else:
        db.session.delete(book)
        db.session.commit()
    return jsonify(response)
    