from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError, IntegrityError
from datetime import datetime

app = Flask(_name_)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root123@localhost/flask_crud_db2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False