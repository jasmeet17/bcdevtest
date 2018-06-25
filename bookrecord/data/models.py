from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, inspect

db = SQLAlchemy()

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
    
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }