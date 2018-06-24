from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask_sqlalchemy import Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import re
import json
# from flask_sqlalchemy import exc
from helper import Helper

CRED_FILE = 'credentials.json'
read_creds = open(CRED_FILE, 'r')
creds = json.load(read_creds)

END_POINT = creds['END_POINT']
USER_NAME = creds['USER_NAME']
PASSWORD = creds['PASSWORD']

REQUEST_SUCCESS = {'success': True}
REQUEST_FAIL = {'success': False, 'error':''}

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+ USER_NAME + ':' + PASSWORD + '@' + END_POINT
db = SQLAlchemy(app)


class Users(db.Model):
    __table__name = 'users'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    user_name = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    password = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)
    access = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)

    def __repr__(self):
        return self.user_name


class Books(db.Model):
    __table__name = 'books'
    isbn = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    author = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    genre = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    price = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    
    def __repr__(self):
        return self.isbn


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
    print type(books)
    print len(books)
    print type(books[0])

    for book in books:
        print book.isbn, book.title, book.author, book.genre, book.price
    return "books"

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


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run()
    