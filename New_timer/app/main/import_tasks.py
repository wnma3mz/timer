# !/usr/bin/python
# -*-coding:utf-8 -*-
# author:Lu
import pymysql

class import_tasks(object):

    def __init__(self):
        pass

    def import_vacation(self, id):
        vacation_list = [['国庆节', '2017-10-01'], ['双十一', '2017-11-11'], ['圣诞节', '2017-12-25'], ['元旦', '2018-01-01'],
                         ['寒假', '2018-01-29']]
        db = pymysql.connect(host='localhost', user='root', password='centos@lu', database="timer", charset='utf8')
        curs_insert = db.cursor()
        for name, date in vacation_list:
            sql_insert = "INSERT INTO task (task_name, task_date, task_num) VALUES (\'%s\', \'%s\', %d)" % (name, date, id)
            curs_insert.execute(sql_insert)
            db.commit()
        db.close()

def delete_repeat():
    tmp_list = []
    db = pymysql.connect(host='localhost', user='root', password='123', database="timer", charset='utf8')
    curs_select = db.cursor()
    curs_del = db.cursor()
    sql_select = 'select * from task a where (a.task_name, a.task_num) in (select task_name,task_num from task group by task_name,task_num having count(*) > 1)'
    curs_select.execute(sql_select)
    for row in curs_select:
        if [row[1], row[5]] in tmp_list:
            sql_del = 'delete from task where (task_name=\'%s\' and task_num=%d) limit 1' % (row[1], row[5])
            curs_del.execute(sql_del)
            db.commit()
        else:
            tmp_list.append([row[1], row[5]])
    db.close()

def import_vacation(studentid):
    vacation_list = [['国庆节', '2017-10-01'], ['双十一', '2017-11-11'], ['圣诞节', '2017-12-25'], ['元旦', '2018-01-01'], ['寒假', '2018-01-29']]
    db = pymysql.connect(host='localhost', user='root', password='123', database="timer", charset='utf8')
    # curs_id = db.cursor()
    curs_insert = db.cursor()
    # sql_id = "SELECT id FROM users WHERE studentid=%s" % studentid
    # curs_id.execute(sql_id)
    # print curs_id.fetchall()
    # id = curs_id.fetchall()[0][0]

    for name, date in vacation_list:
        sql_insert = "INSERT INTO task (task_name, task_date, task_num) VALUES (\'%s\', \'%s\', %d)" % (name, date, id)
        curs_insert.execute(sql_insert)
        db.commit()
    db.close()
if __name__ == '__main__':
    import_vacation(5710116133)
