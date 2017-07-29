# !/usr/bin/python
# -*-coding:utf-8 -*-
# author:Lu
import time
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DateTimeField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Length


def time_del(str_input):
    str1 = time.mktime(time.strptime(str_input, '%Y-%m-%d'))
    str2 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    str2 = time.mktime(time.strptime(str2, '%Y-%m-%d'))
    if str2 > str1:
        return False
    else:
        return True



class LoginForm(FlaskForm):
    studentid = StringField(u'学号', validators=[DataRequired(message=u'请正确输入你的学号'), Length(10),])
    password = PasswordField(u'密码', validators=[DataRequired(message= u'请输入你的密码')])
    submit = SubmitField(u'登录')


class Edit_Form(FlaskForm):
    task_name = StringField(u'事件', validators=[DataRequired(message= u'请填写事件名')])
    task_date = DateTimeField(u'日期', format='%Y-%m-%d', validators=[DataRequired(message= u'请填写事件日期')])
    task_detail = TextAreaField(u'事件内容')
    submit = SubmitField(u'提交')

    def validate_task_date(self, field):
        date = str(field.data)[0:10]
        if not time_del(date):
            raise ValidationError(u'日期错误.')
