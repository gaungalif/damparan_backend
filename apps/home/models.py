from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


from apps import db, ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Integer, nullable=False, default=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    moderator = db.Column(db.Integer, nullable=False, default=False)
    active = db.Column(db.Integer, nullable=False, default=False)
    token = db.Column(db.String(255))