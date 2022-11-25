import pymysql


# connection 객체 생성
conn=pymysql.connect(user='root',
            password='1234',
            host='localhost',
            db='food_ordering_system',
            charset='utf8')

# 커서 객체 연결
curs=conn.cursor() 


print('\n\n')

print("###1-3###")
print('Enter the code of the restaurant you are curious about if there is an expensive menu than all the menus in ‘AAAAAAAB’ ')
flag=1
res_name=input('restaurant: ')
# 존재하는 레스토랑인지 check

sql3_3="select * from restaurant where restaurant_code=%s"
curs.execute(sql3_3,res_name)
flag=curs.fetchone()

if flag:
    sql3="select menu_name from menu where restaurant_code=%s and menu_price > all(select menu_price from menu where restaurant_code= 'AAAAAAAB') "
    curs.execute(sql3,res_name)
    sql3_result=curs.fetchall()
    if sql3_result:
        print('results are below: ')
        for x in sql3_result:  
            print(x[0])
    else:
        print('no more expensive menu than AAAAAAAB')



    

    



