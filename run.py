from flask import Flask, session, render_template, redirect, request, url_for
from database import (Database,login,signup,order)
from user import User,Order
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
    res_list=order().show_rest()


    if request.method=='POST':
        res_list=order().show_rest()
        restaurant_code=request.form.get('restaurant')

        if order().restaurant_code_exists(restaurant_code):
            Order.restaurant_code=restaurant_code
            
            Order.res_name=order().get_restaurant_name(restaurant_code)
            return redirect(url_for('ordermenu'))

        else:
            error='존재하지 않는 식당 코드입니다.'

    return render_template('restaurant.html',res_list=res_list,error=error,restaurant_name=Order.res_name)

@app.route('/ordermenu',methods=['GET','POST'])
def ordermenu():
    error=None
    menu_list=order().show_menu(Order.restaurant_code)
    amount_list=[]
    cost=[]
    total_cost=0
    minimum_amount=order().minimum_price(Order.restaurant_code) # 최소주문금액

    if request.method=='POST':
        menu_list=order().show_menu(Order.restaurant_code)
        Order.res_name=order().get_restaurant_name(Order.restaurant_code)
        Order.minimum_amount=minimum_amount

        lst=order().show_menu_list(Order.restaurant_code) # 가게 메뉴 리스트
        lst2=[]
        amount_list=[]
        for x in lst:
            if request.form.get(x):
                lst2.append(x) # 주문받은 메뉴 저장
                amount=request.form.get('amount')
                amount_list.append(amount) #수량 받아서 리스트에 저장

        cost=order().calculate_cost(lst2,amount_list) # 각 메뉴마다 금액
        total_cost=sum(cost)
        if order().compare_minimum_price(total_cost,Order.restaurant_code): #최소주문금액만족
            return (redirect(url_for('home'))) # 주문목록 확인 및 결제창

        else:
            error='최소주문금액은'+str(Order.minimum_amount)+',주문금액은'+str(total_cost)


    return render_template('ordermenu.html',error=error,restaurant_name=Order.res_name,minimum_amount=minimum_amount,menu_list=menu_list )

        
            
            
            


if __name__=='__main__':
    app.run(port=5000,debug=True)
