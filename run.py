from flask import Flask, session, render_template, redirect, request, url_for
from database import (Database,login,signup,order)
#from flask_sqlalchemy import SQLAlchemy
from user import User,Order
#from helloflask.model import Members
app=Flask(__name__)


# 로그인 잘못했을 때 어떻게 할지...
#
@app.route('/',methods=['GET','POST'])
def main(): 
    error=None # 넘겨줄 변수 
    success=None

    if request.method=='POST':
        email=request.form.get('email')
        pw=request.form.get('pw')

        if login().compare_data(email,pw):
            User.email=email
            User.pw=pw
            User.name=Database().load_user_name(email)
            User.phone_number=Database().load_user_phonenum(email)
            #return redirect(url_for('home'))
            # dict 형태로 user 정보 전달하기 
            success='로그인 성공!'
            return redirect(url_for('select'))
        else:
            error='존재하지 않는 이메일 또는 비밀번호입니다.'
            

    return render_template('main.html',success=success,error=error)

@app.route('/register',methods=['GET','POST'])
def register(): # 성공하면 redirect(url_for('login'))
    error=None
    success=None

    if request.method=='POST':
        name=request.form.get('name')
        phonenumber=request.form.get('phonenumber')
        email=request.form.get('email')
        pw=request.form.get('pw')

        if Database().email_not_exists(email): # 가입가능
            # signup().add_email_data(email)
            signup().add_user_info(email,name,phonenumber)
            signup().add_password(email,pw)
            

            User.name=name
            User.email=email
            User.pw=pw
            User.phone_number=phonenumber
            success='회원가입 성공!'
            return redirect(url_for('main'))

        else:
            error='존재하는 이메일입니다'

    return render_template('register.html',success=success,error=error)

@app.route('/home',methods=['GET','POST'])
def home():
    
    return render_template('home.html',name=User.name)

    

@app.route('/select',methods=['GET','POST'])
def select():  
    error=None 
    res_list=[]


    if request.method=='POST':
        res_list=order().show_rest()
        restaurant_code=request.form.get('restaurant')

        if order().restaurant_code_exists(restaurant_code):
            Order.restaurant_code=restaurant_code
            
            Order.res_name=order().get_restaurant_name(restaurant_code)
            return redirect(url_for('home'))

        else:
            error='존재하지 않는 식당 코드입니다.'

    return render_template('restaurant.html',res_list=res_list,error=error,restaurant_name=Order.res_name)

if __name__=='__main__':
    app.run(port=5000,debug=True)
