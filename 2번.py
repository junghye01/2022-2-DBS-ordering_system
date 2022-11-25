import datetime 

import mysql.connector 

cnx = mysql.connector.connect(user='root', password='@hyungsuk1234', host='127.0.0.1', database='food_ordering_system', charset='utf8') 

cursor = cnx.cursor()
    
#From here, we will use FindRes function which we've made.
name=input("Search Restaurant: ")
query=("select FindRes('"+name+"');")
cursor.execute(query)
rows=cursor.fetchall()
r_code=''.join(rows[0])#convert tuple to string
print("restaurant_code: "+r_code) #Shows restaurant_code which you searched for
#End of using function

#Form here, we will use test procedure which we've made
query = ("call test('"+r_code+"',@result);")
cursor.execute(query)
query=("select @result as count;")
cursor.execute(query)
result=cursor.fetchall()
print("Number of orders: "+str(result[0][0]))#Shows the number of orders received at the restaurant
#End of using procedure

cursor.close()
cnx.close() 

