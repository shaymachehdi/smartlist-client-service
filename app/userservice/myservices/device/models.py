from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, types,JSON,Float
from datetime import datetime
from userservice import db
from werkzeug import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin




# Device Model

class Device(UserMixin,db.Model):
    idDevice = db.Column(db.Integer, primary_key=True)
    localisation = db.Column(JSON)
    code_device=db.Column(db.String(200))
    email = db.Column(db.String(200))
    install_at = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('registreduser.id'), nullable=True)
    levelConfidence_device=db.Column(db.Float, default=0)

    # Init constructor
    def __init__(self, localisation, email,install_at,code):
        self.localisation = localisation
        self.install_at = install_at
        self.email = email
        self.code_device=code