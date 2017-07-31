# !/usr/bin/python
# -*-coding:utf-8 -*-
# author:Lu

from app import create_app

application = create_app('production')

if __name__ == '__main__':
    application.run()