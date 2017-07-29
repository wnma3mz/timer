本应用为天数倒计时应用
结合教学周历和考试安排综合开发的web页面

主要含有用户注册登录修改个人信息、自定义任务倒计时、自动导入教学周历、期末考试安排的功能

目录结构如下

├── app
│   ├── auth
│   │   ├── errors.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── views.py
│   ├── email.py
│   ├── __init__.py
│   ├── main
│   │   ├── errors.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── views.py
│   ├── models.py
│   ├── static
│   │   └── styles.css
│   └── templates
│       ├── 404.html
│       ├── 500.html
│       ├── auth
│       │   ├── change_email.html
│       │   ├── change_password.html
│       │   ├── edit_auth.html
│       │   ├── email
│       │   │   ├── change_email.html
│       │   │   ├── change_email.txt
│       │   │   ├── confirm.html
│       │   │   ├── confirm.txt
│       │   │   ├── reset_password.html
│       │   │   └── reset_password.txt
│       │   ├── login.html
│       │   ├── register.html
│       │   ├── reset_password.html
│       │   └── unconfirmed.html
│       ├── base.html
│       ├── details.html
│       ├── edit_task.html
│       ├── index.html
│       └── task_list.html
├── config.py
├── import_tasks.py
├── manage.py
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 15bc73784bee_.py
│       ├── 7bbfdf360447_.py
├── README.md
└── requirements.txt

manage.py
用于启动app
包含Manager、Migrate
（模板代码）

import_tasks.py
用户导入教学周历的tasks
方法：连接数据库对数据库进行增改


config.py
配置文件设置
class Config
    SECRET_KEY
    SQLALCHEMY
    MAIL

class DevelomentConfig
    MAIL 163
    SQLALCHEMY

class ProductionConfig
    SQLALCHEMY

class HerokuConfig
    Mail

config = {}

app/
    __init__.py
    导入Bootstrap、Mail、SQLAlchemy、LoginManager
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    email.py
    异步发送邮件(固定模板)

    models.py
    定义数据库模型
    User
        id、email、username、password、task、confirmed、password_hash
        验证密码：password、verify_password
        验证账号：confirm、generate_confirmation_token、generate_email_change_token、generate_reset_token
        获取时间：ping
        重置账号密码：change_email、reset_password

    Task
        task_id、task_name、task_date、task_detail、day_dis、task_num

    auth/
        __init__.py(模板)
        errors.py(模板)
        forms.py(表单)
            LoginForm：登陆界面表单
            RegistrationForm：注册界面表单
            ChangePasswordForm：更改密码表单
            PasswordResetRequestForm：忘记密码申请重置表单
            PasswordResetForm：忘记密码重置表单
            ChangeEmailForm：更改邮箱表单

        views.py(视图)
            register：注册
            login：登陆
            logout：登出
            confirm：验证账户
            before_request：账户登陆、账户还未验证成功 -> unconfirmed：验证失败，需重新验证
            resend_confirmation：重新验证
            before_request：验证获取时间
            change_password：修改密码
            password_reset_request：忘记密码的请求
            password_reset：忘记密码重置
            change_email_request：修改邮箱的请求
            change_email：修改邮箱

        用户名中必须有一个字母，开头不能使用下划线、小数点、字母
        要求用户邮箱有唯一性、用户名也要求唯一性

    main/
        __init__.py(模板)
        errors.py(模板)
        forms.py(表单)
            Edit_Form：新建\编辑任务表单

        views.py(视图)
            index：首页（导航页）
            task_list：显示所有任务（任务名、日期、剩余天数、升序排列、可跳转至详情页、编辑页、新建页，可以直接删除任务，）
            new_task：新建任务（任务名、日期必填、详情选填）
            delete_task：删除任务
            edit_task：编辑任务（更改任务某项或多项）
            task_detail：任务详情（显示一项任务的所有信息，并由此可以跳转至编辑页、也可以直接删除）
            import_exam：导入考试

            规定所有任务名不得重复
            修改任务时、若与原来信息相同则进行提示

    templates/
        404.html：错误页面
        500.html：错误页面
        base.html：模板页
        details.html：任务详情页
        edit_task.html：新建\编辑页
        index.html：首页（导航页）
        task_list.html：所有任务显示页

        auth/
            change_email.html：修改邮箱页
            change_password.html：修改密码页
            login.html：登陆页
            register.html：注册页
            reset_password.html：重置密码（请求页+重设页）
            unconfirmed.html：未验证用户登陆页

            email/
                change_email.html：修改邮箱发送的邮件
                confirm.html：验证账号发送的邮件
                reset_password.html：重置密码发送的邮件