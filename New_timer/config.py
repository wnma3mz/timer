#!/usr/bin/python
# -*-coding:utf-8 -*-
# author:Lu
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class DevelomentConfig(Config):
    # DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123@localhost:3306/timer'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123@localhost:3306/timer'

class HerokuConfig(Config):
    # DEBUG = True
    pass



config = {
    'development': DevelomentConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelomentConfig,
}
