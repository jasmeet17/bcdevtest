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
from bookrecord.controllers.books import allBooks
from bookrecord.controllers.addUser import addUserController
from bookrecord.controllers.updateRating import updateRatingController
from bookrecord.controllers.addBook import addBookController
from bookrecord.controllers.removeBook import removeBookController
from bookrecord.utils import get_instance_folder_path
from bookrecord.config import configureApp
import copy

"""Initial Configuration"""
app = Flask(__name__,instance_path=get_instance_folder_path(),
            instance_relative_config=True)
db.init_app(app)
configureApp(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found - 404'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request - 400'}), 400)

@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify(copy.deepcopy(Helper.REQUEST_SUCCESS))

@app.route("/books", methods=["GET", "POST"])
def books():
    return allBooks()

@app.route("/add_user", methods=["POST"])
def addUser():
    """Add a user in the Database"""
    return addUserController(request)

@app.route("/update_rating", methods=["PUT"])
def updateRating():
    """Update rating of a book"""
    return updateRatingController(request)

@app.route("/add_book", methods=["POST"])
def addBook():
    """Add a Book in the Database, if User has Access"""
    return addBookController(request)

@app.route("/remove_book", methods=["DELETE"])
def removeBook():
    """Remove book form the Batabase, If user has Access"""
    return removeBookController(request)