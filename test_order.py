from datetime import date
import pymysql
from database import order

data='asi' # 이방식은 겹침.. 
hash_list=[]
for i in range(len(data)):
    result=ord(data[i])
    result=result%3
    result=str(result)
    hash_list.append(result)

hash_result="".join(hash_list)
print(hash_result)

s='7260b361e0a26d24cd9602b4e84ba811'
print(len(s))
s1='ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb'
print(len(s1))

today=(date.today())
#print(today.type())

myconnect=pymysql.connect(user='root',
            password='1234',
            host='localhost',
            db='food_ordering_system',
            charset='utf8')
curs=myconnect.cursor()
sql="select * from menu"
curs.execute(sql)
data=curs.fetchall()
lst=[]
for x in data:
    lst.append(x[2])

print(lst)


res_list=order().show_rest()

for x in res_list:
    print(x[0],x[1])
restaurant_code='AAAAAAAB'
min_price=order().minimum_price(restaurant_code)
#print(min_price)
my_menu=order().show_menu_list(restaurant_code)
print(my_menu)
for x in my_menu:
    print(x)
