from menu import Menu, Order_table
from database import (Database,signup,login,order)


userselection=int(input('로그인은 1번, 회원가입은 2번: '))

initialmenu=True
while(initialmenu):
    if userselection==1:
        if Menu().login_sign_menu(userselection):
            Menu().load_user_data
            initialmenu=False
        else:
            userselection=1
            #print('다시 입력하세요')
    elif userselection==2:
        if Menu().login_sign_menu(userselection):
            userselection=1
        else: #회원가입 실패
            userselection=2
            #print('다시 시도하세요')

#여기부턴 주문
import datetime 

import mysql.connector 

cnx = mysql.connector.connect(user='root', password='@hyungsuk1234', host='127.0.0.1', database='food_ordering_system', charset='utf8') 

cursor = cnx.cursor()
order_status=True
order_code='E01503M0'
sql="select * from restaurant;"
cursor.execute(sql)
res_list=cursor.fetchall()
count=0
for res in res_list:
    cnt=str(count+1)
    print(cnt+"번 "+res[1]) 
    count=count+1
            
userselection=int(input('원하는 음식점의 번호를 누르세요(뒤로가기는 0번): '))
print(res_list[userselection-1][1])
res=res_list[userselection-1][1]
res_code=res_list[userselection-1][0]
sql="select * from menu where restaurant_code in (select r.restaurant_code from restaurant as r where r.restaurant_name='"+res+"');"
#선택한 식당의 메뉴 보여주는 sql문
cursor.execute(sql)
menu_list=cursor.fetchall()
count=0
price=0 #총 가격
userselection=-1
while(userselection!=0):
    for m in menu_list: #선택한 식당 메뉴 하나씩
        cnt=str(count+1)
        name=m[2]#메뉴이름
        desc=m[3]#메뉴 설명
        price=str(m[4])#메뉴 가격
        print(cnt+"번 "+name+" "+desc+" "+price)#메뉴 하나 출력
        count=count+1
    userselection=int(input('원하는 메뉴의 번호를 누르세요(주문하기는 0번): '))
    amount=int(input('수량을 입력하세요: '))
    res_code=res_list[userselection-1][0]#식당 코드
    menu_code=menu_list[userselection-1][0]#메뉴 코드
    cost=price*amount #메뉴가격x수량 
    order().add_order_menu(order_code,res_code,menu_code,amount,price) #order_menu 엔티티에 추가
    #반복    
#0번이 눌리면
if(Order_table().order_table(order_code,res_code)):#menu 파일에 있음
    userselection=input("주문완료는 0번")
    
