import datetime 

import mysql.connector
from database import Database,payment

cnx = mysql.connector.connect(user='root', password='@hyungsuk1234', host='127.0.0.1', database='food_ordering_system', charset='utf8') 

cursor = cnx.cursor()
order_code=input("주문코드")
total=payment().get_total(order_code)
print(total)

order_code=input("주문코드")
sql="SELECT sum(price) from order_menu where order_code=%s"
cursor.execute(sql,order_code)
total=cursor.fetchone()
print(total)

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
print(type(res_list[userselection-1][1]))
res=res_list[userselection-1][1]
sql="select * from menu where restaurant_code in (select r.restaurant_code from restaurant as r where r.restaurant_name='"+res+"');"
cursor.execute(sql)
menu_list=cursor.fetchall()
count=0
for menu in menu_list:
    cnt=str(count+1)
    name=menu[2]
    desc=menu[3]
    p=menu[4]
    print(type(p))
    price=str(p)
    print(cnt+"번 "+name+" "+desc+" "+price)
    count=count+1

cursor.close()
cnx.close() 

