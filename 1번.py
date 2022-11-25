import pymysql


# connection 객체 생성
conn=pymysql.connect(user='root',
            password='1234',
            host='localhost',
            db='food_ordering_system',
            charset='utf8')

# 커서 객체 연결
curs=conn.cursor() 



print("###1-1###")
print('Find all order codes for the date entered')
date=input('date:')
sql1="select order_code from `order` where date=%s"
curs.execute(sql1,date)
sql1_result=curs.fetchall()
if sql1_result:
    for x in sql1_result:
        print(x[0])
else:
    print('There are no orders on that date')
print('\n\n')

print("###1-2###")
print('Enter two tables which you want to Natural join')

table1,table2=input('enter two tables separated by " ":').split() 
tables=[]
sql2_2="show tables"
curs.execute(sql2_2)
table_result=curs.fetchall()
for x in table_result:
    tables.append(x[0])

if table1 in tables and table2 in tables: # table 목록에 존재하는 table이면
    sql2="select * from {0} natural join {1}".format(table1,table2)
    curs.execute(sql2)
    sql2_result=curs.fetchall()
    if sql2_result:
        for x in sql2_result:
                print(x)
    else:
        print('there is no common attribute')
else:
    print('table name does not exist')
    




print('\n\n')
print("###1-3###")
print('Enter the code of the restaurant you are curious about if there is an expensive menu than all the menus in ‘AAAAAAAB’ ')
res_code=input('restaurant code: ')
# 존재하는 레스토랑인지 check

sql3_3="select * from restaurant where restaurant_code=%s"
curs.execute(sql3_3,res_code)
flag=curs.fetchone()
if flag:
    sql3="select menu_name from menu where restaurant_code=%s and menu_price > all(select menu_price from menu where restaurant_code= 'AAAAAAAB') "
    curs.execute(sql3,res_code)
    sql3_result=curs.fetchall()
    if sql3_result:
        print('results are below: ')
        for x in sql3_result:  
            print(x[0])
    else:
        print('no more expensive menu than AAAAAAAB')

else:
    print('no restaurant code exists')









print('\n\n')
print("###1-4###")

rest_name=input('enter the restaurant name you want to change the location to: ')
rest_address=input('location:')
#존재하는 레스토랑인지 check
sql3_3="select * from restaurant where restaurant_name=%s"
curs.execute(sql3_3,rest_name)
flag=curs.fetchone()
if flag:
    sql4="UPDATE restaurant set restaurant_location=%s where restaurant_name=%s"
    curs.execute(sql4,(rest_address,rest_name))
    conn.commit()

    # update 내용 확인하기
    print('Print out changes: ')
    sql4_4="SELECT * FROM restaurant where restaurant_name=%s"

    curs.execute(sql4_4,rest_name)
    data=curs.fetchone()
    print(data)

else:
    print('no restaurant name exists')

curs.close()