# !/usr/bin/python
# -*-coding:utf-8 -*-
# author:Lu

from flask_login import UserMixin
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.String(64))
    password = db.Column(db.String(64))
    college = db.Column(db.String(128))
    class_ = db.Column(db.String(128))
    task = db.relationship('Task', backref='users')



class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(64))
    task_date = db.Column(db.String(64))
    task_detail = db.Column(db.UnicodeText, unique=False, nullable=True)
    day_dis = db.Column(db.Integer)
    task_num = db.Column(db.Integer, db.ForeignKey('users.id'))


