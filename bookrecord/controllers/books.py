from flask import jsonify
import copy
from bookrecord.helper import Helper
from bookrecord.data.models import db, Books

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