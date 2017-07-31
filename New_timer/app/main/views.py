# !/usr/bin/python
# -*-coding:utf-8 -*-
# author:Lu
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import db
from app.main.forms import Edit_Form, LoginForm
from app.models import Task, User
from . import main
import time
import requests
from . import import_tasks

s = requests.Session()

def jisuan(str_input):
    str1 = time.mktime(time.strptime(str_input, '%Y-%m-%d'))
    str2 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    str2 = time.mktime(time.strptime(str2, '%Y-%m-%d'))
    return int(int(str1 - str2) / 3600 / 24)

def import_exam_list(studentID):
    pass

def input_flash(name, ustr):
    db.session.add(name)
    db.session.commit()
    flash(ustr)

def login_ncuos(studentid, password):

    data = {
        "username": studentid,
        "password": password,
    }
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
        "Host": "ncuos.com",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://ncuos.com/loginBox/login",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    }

    url_api = 'http://ncuos.com/api/user/token'
    response = s.post(url_api, json=data)
    try:
        token = "passport " + response.json()["token"]
        header["Authorization"]= token

        url_verify = 'http://ncuos.com/api/user/profile/school_roll'
        info = s.get(url_verify, headers=header).json()
        college, class_ =  info["school_roll"][1]["xy"], info["school_roll"][1]["bjmc"]
        # print(college, class_)
        return college, class_
    except:
        return None, None

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        studentid = str(form.studentid.data)
        password = str(form.password.data)
        user = User.query.filter_by(studentid=studentid).first()
        # print user.college
        college, class_ = login_ncuos(studentid, password)
        if college == None:
            flash(u"请正确输入你的学号或者密码")
            return render_template('login.html', form=form)
        else:
            if user != None:
                user.college, user.class_, user.password = college, class_, password
                db.session.add(user)
                db.session.commit()
            else:
                user = User(studentid=studentid,
                            password=password,
                            college=college,
                            class_=class_)
                db.session.add(user)
                db.session.commit()
                user = User.query.filter_by(studentid=studentid).first()
                im = import_tasks.import_tasks()
                im.import_vacation(user.id)
            login_user(user, remember=True)
            flash(u'登录成功')
            return redirect(url_for('main.task_list'))
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'你已登出.')
    return redirect(url_for('main.login'))

@main.route('/', methods=['GET', 'POST'])
@main.route('/task_list', methods=['GET', 'POST'])
@login_required
def task_list():
    id = current_user.id
    tasks = Task.query.filter_by(task_num=id)
    for task in tasks:
        task.day_dis = jisuan(task.task_date)
        if task.day_dis >= 0:
            db.session.add(task)
        else:
            db.session.delete(task)
        db.session.commit()
    tasks = db.session.query(Task).filter_by(task_num=id).order_by(Task.day_dis)
    return render_template('task_list.html', tasks=tasks)

@main.route('/new_task', methods=['GET', 'POST'])
@login_required
def new_task():
    form = Edit_Form()
    if form.validate_on_submit():
        if Task.query.filter_by(task_name=form.task_name.data, task_num=current_user.id).first():
            flash(u'已存在事件.')
            return render_template('new_task.html', form=form)
        task_date = str(form.task_date.data)[0:10]
        id = current_user.id
        day_dis = jisuan(task_date)
        task = Task(task_name=form.task_name.data,
                    task_date=task_date,
                    day_dis=day_dis,
                    task_detail=form.task_detail.data,
                    task_num=id)
        input_flash(task, u'提交成功')
        return redirect(url_for('main.task_list'))
    return render_template('new_task.html', form=form)

@main.route('/delete_task/<Tname>', methods=['GET', 'POST'])
@login_required
def delete_task(Tname):
    task = Task.query.filter_by(task_name=Tname, task_num=current_user.id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.task_list'))

@main.route('/edit_task/<Tname>', methods=['GET', 'POST'])
@login_required
def edit_task(Tname):
    form = Edit_Form()
    id = current_user.id
    task = Task.query.filter_by(task_name=Tname, task_num=id).first()
    if form.validate_on_submit():
        task_date = str(form.task_date.data)[0:10]
        day_dis = jisuan(task_date)
        task.day_dis = day_dis
        if Tname == form.task_name.data:
            if form.task_detail.data == task.task_detail and task_date == task.task_date:
                flash(u'未修改')
                return render_template('edit_task.html', form=form, task=task)
            task.task_name, task.task_date, task.task_detail = form.task_name.data, task_date, form.task_detail.data
            input_flash(task, u'修改成功')
            return redirect(url_for('main.task_list'))
        else:
            if Task.query.filter_by(task_name=form.task_name.data, task_num=id).first():
                flash(u'已存在事件.')
                return render_template('edit_task.html', form=form, task=task)
            task.task_name, task.task_date, task.task_detail = form.task_name.data, task_date, form.task_detail.data
            input_flash(task, u'修改成功')
            return redirect(url_for('main.task_list'))
    return render_template('edit_task.html', form=form, task=task)

@main.route('/task_detail/<Tname>', methods=['GET', 'POST'])
@login_required
def task_detail(Tname):
    task = Task.query.filter_by(task_name=Tname, task_num=current_user.id).first()
    if task.task_detail:
        task_detail = task.task_detail.split("\r\n")
    else:
        task_detail = ""
    return render_template('details.html',
                           task_name=task.task_name,
                           day_dis=task.day_dis,
                           task_date=task.task_date,
                           task_detail=task_detail)

@main.route('/import_exam', methods=['GET', 'POST'])
@login_required
def import_exam():
    # stdutentID = current_user.username
    pass
    # import_exam_list()
    return redirect(url_for("main.task_list"))
