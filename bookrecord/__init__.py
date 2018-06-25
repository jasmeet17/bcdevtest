from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, inspect
import re
import os
import json
from helper import Helper
from bookrecord.data.models import db, Users, Books
from bookrecord.utils import get_instance_folder_path
from bookrecord.config import configureApp
import copy

"""Initial Configuration"""
app = Flask(__name__,instance_path=get_instance_folder_path(),
            instance_relative_config=True)
db.init_app(app)
configureApp(app)

"""Handling Bad requests"""
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request - 400'}), 400)

@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify(copy.deepcopy(Helper.REQUEST_SUCCESS))

@app.route("/books", methods=["GET", "POST"])
def books():
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

@app.route("/add_user", methods=["POST"])
def addUser():
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

@app.route("/update_rating", methods=["PUT"])
def updateRating():
    response = copy.deepcopy(Helper.REQUEST_FAIL)
    user_name = request.json.get('user_name')
    password = request.json.get('password')

    if user_name is None and password is None:
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

@app.route("/add_book", methods=["POST"])
def addBook():
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

@app.route("/remove_book", methods=["DELETE"])
def remove():
    """Remove book form the Batabase, If user has Access"""
    response = copy.deepcopy(Helper.REQUEST_FAIL)
    user_name = request.json.get('user_name')
    password = request.json.get('password')

    if user_name is None and password is None:
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

def hasUpdateAccess(user_name, password):
    user = Users.query.filter_by(user_name=user_name,password=password).first()

    if user!=None and user.access==0:
        return True
    return False