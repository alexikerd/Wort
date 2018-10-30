from sqlalchemy import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path

database_path = "sqlite:///database/Wuerze.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_path

db = SQLAlchemy(app)

e = create_engine(database_path)