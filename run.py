from flask import Flask, session, render_template, redirect, request, url_for
from database import (Database,login,signup,order)
from user import User,Order
from datetime import date
app=Flask(__name__)



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



@app.route('/select',methods=['GET','POST'])
def select():  
    error=None 
    res_list=order().show_rest()


    if request.method=='POST':
        res_list=order().show_rest()
        restaurant_code=request.form.get('restaurant')
        
        if order().restaurant_code_exists(restaurant_code): # 존재하면

            Order.restaurant_code=restaurant_code #레스토랑 코드
            Order.minimum_amount=order().minimum_price(Order.restaurant_code) # 최소주문금액
            Order.res_name=order().get_restaurant_name(Order.restaurant_code) # 레스토랑 이름
            return redirect(url_for('ordermenu'))
        else: # 잘못 입력한 경우
            error="존재하지 않는 레스토랑 코드입니다"

       

    return render_template('restaurant.html',res_list=res_list,restaurant_name=Order.res_name,error=error)

@app.route('/ordermenu',methods=['GET','POST'])
def ordermenu():
    error=None
    menu_list=order().show_menu(Order.restaurant_code)
    
    #total_cost=0
    
    if request.method=='POST':
        menu_list=order().show_menu(Order.restaurant_code)
        Order.res_name=order().get_restaurant_name(Order.restaurant_code)
        

        lst=order().show_menu_list(Order.restaurant_code) # 가게 메뉴 리스트
        lst2=[]
        
        amount_list=[]
        for x in lst:
            if request.form.get(x):
                lst2.append(x) # 주문받은 메뉴 저장
                
            else:
                continue

        for i in range(len(lst)):
            t_name=lst[i]+'1'
            amount=request.form.get(t_name)
            if amount:
                amount_list.append(amount)
            else:
                continue
        
        #메뉴,수량 배열
        Order.final_list=[]
        new_list=[]
        for i in range(len(lst2)):
            new_list=[lst2[i],amount_list[i]]
            Order.final_list.append(new_list)
                
        
        
        cost=order().calculate_cost(lst2,amount_list) # 각 메뉴마다 금액
        
        Order.total_cost=sum(cost) # 총 주문금액
        
        
        if order().compare_minimum_price(Order.total_cost,Order.restaurant_code): #최소주문금액만족
            Order.order_code=order().make_ordercode(User.email) #주문코드 생성
            # order 테이블에 저장
            Order.date=date.today()
            order().add_order_data(Order.order_code,User.email,Order.date,Order.restaurant_code)
            # 
            Order.menu_code=order().get_menucode(lst2)
            for i in range(len(lst2)): # 메뉴 하나씩 order_menu테이블에 저장
                order().add_order_menu(Order.order_code,Order.menu_code[i],amount_list[i],cost[i])


            return (redirect(url_for('final'))) # 요청사항,결제수단 입력 창으로 이동

        else:
            error='최소주문금액은'+str(Order.minimum_amount)+',주문금액은'+str(Order.total_cost)


    return render_template('ordermenu.html',error=error,restaurant_name=Order.res_name,minimum_amount=Order.minimum_amount,menu_list=menu_list )

        
            
@app.route('/final',methods=['GET','POST'])
def final():
    
  
    coupon_list=order().show_coupon_code()
    if request.method=='POST':
        address=request.form.get('address')
        textrequest=request.form.get('textrequest')
        payment=request.form.get('payment')
        coupon_code=request.form.get('coupon_code')

        
        Order.discount_price=order().get_discount(coupon_code)
        
        Order.payment_amount=Order.total_cost-Order.discount_price # payment_amount : 결제금액
        Order.address=address
        Order.textrequest=textrequest
        Order.payment=payment
        #order 테이블엔 address,request,coupon_code update
        order().update_order(Order.order_code,address,textrequest,coupon_code)
        #payment에는 다 insert
        order().add_payment_data(Order.order_code,payment,Order.total_cost)
        return redirect(url_for('realfinal'))




    return render_template('order.html',order_code=Order.order_code,email=User.email,date=Order.date,restaurant_code=Order.restaurant_code,coupon_list=coupon_list)

@app.route('/realfinal',methods=['GET','POST'])
def realfinal():
    
 
    return render_template('home.html',name=User.name,order_code=Order.order_code,address=Order.address,textrequest=Order.textrequest,payment=Order.payment,final_list=Order.final_list,total_cost=Order.total_cost,discount_price=Order.discount_price,payment_amount=Order.payment_amount)



if __name__=='__main__':
    app.run(port=5000,debug=True)