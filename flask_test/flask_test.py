'''
flask服务器
    使用静态文件
    蓝图是啥
    模板：jinjia2模板引擎
'''

from flask import Flask, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField,SubmitField
from wtforms.validators import Required, DataRequired


# 创建一个表单的类继承自flaskform
class LoginForm(FlaskForm):
    # 问题：这里的提示信息无法显示
    name=StringField(label='用户名',validators=[DataRequired('用户名不能为空')])
    pwd = PasswordField(label='密码', validators=[DataRequired('密码不能为空')])
    submit=SubmitField(label='提交')


# 创建实例，第一个参数是应用模块或包的名称，单一模块用__name__。告诉flask到哪里找模板、静态文件。
app=Flask(__name__)
app.config['SECRET_KEY']='mimi'

# 装饰器，把修饰的函数注册为路由，告诉flask啥样的url能触发函数
@app.route('/',methods=['GET','POST'])
def index():
    form=LoginForm()
    data={}
    if form.validate_on_submit():
        data['name']=form.name.data
        data['pwd']=form.pwd.data
    # 打开主页模板文件
    return render_template('index.html',form=form,data=data)

# 字符串类型，还有int,float,path（接收斜线）
@app.route('/home/<username>')
def show_user_profile(username):
    # return '你好，%s' % username
    # 打开用户模板文件
    return render_template('home.html',name=username)

# 整数类型
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # 显示用户名
    return 'postid：%s' % post_id


# 构造Url并返回其他方法的激活url
@app.route('/url/')
def get_url():
    return url_for('show_post',post_id=2)
    #使用静态文件可以用：url_for('static',filename='a.css')，需要保存到static文件夹下

# 根据不同方法做出响应，运行不了
# @app.route('login',methods=['GET','POST']):
# def login():
#     if request.method=='POST':
#         pass
#     else:
#         pass


# 作为直接运行的文件时才会调用
if __name__ == '__main__':
    # 打开调试，可以让代码改动后自动重启，并调试错误，两种方法
    # app.debug=True
    app.run(debug=True)