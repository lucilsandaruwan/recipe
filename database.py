'''
This file is created to avoid duplicate code to  import flask_sqlalchemy import SQLAlchemy 
from main files and models
'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Model = db.Model
session = db.session
Column = db.Column
Boolean = db.Boolean
Integer = db.Integer
String = db.String
DateTime = db.DateTime
Text = db.Text
ForeignKey = db.ForeignKey
relationship = db.relationship