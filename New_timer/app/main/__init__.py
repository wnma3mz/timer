# !/usr/bin/python
# -*-coding:utf-8 -*-
# author:Lu

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views