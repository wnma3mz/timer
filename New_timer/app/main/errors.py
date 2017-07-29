# !/usr/bin/python
# -*-coding:utf-8 -*-
# author:Lu
from flask import render_template
from . import main
# 返回404
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 返回500
@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500