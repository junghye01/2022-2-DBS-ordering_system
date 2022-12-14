import pymysql
import bcrypt
from datetime import (date,datetime)
from hashlib import md5

class Database(object):
    def __init__(self):
        self.order_db=pymysql.connect(
            user='root',
            password='1234',
            host='localhost',
            db='food_ordering_system',
            charset='utf8'
        )

    def email_not_exists(self,email_text): # 존재하지 않으면 1
        curs=self.order_db.cursor()
        sql="SELECT * FROM account WHERE user_email= %s"
        curs.execute(sql,email_text)
        data=curs.fetchone()
        if data:
            return 0
        else:
            return 1

    def load_user_name(self,user_email):
        curs=self.order_db.cursor()
        sql="SELECT * FROM user where user_email=%s"
        curs.execute(sql,user_email)
        data=curs.fetchone()
        curs.close()
        result=data[1]

        return result
        

    def load_user_phonenum(self,user_email):
        curs=self.order_db.cursor()
        sql="SELECT * FROM user where user_email=%s"
        curs.execute(sql,user_email)
        data=curs.fetchone()
        curs.close()
        result=data[2]
        return result

# 회원가입
class signup(Database):
    def __init__(self):
        super().__init__()
    

    def add_password(self,user_email,user_password): # insert로 바꿔야됨
        new_salt=bcrypt.gensalt()
        new_pw=user_password.encode('utf-8')
        hashed_pw=bcrypt.hashpw(new_pw,new_salt)# 해시된 비밀번호
        decode_hash_pw=hashed_pw.decode('utf-8')

        curs=self.order_db.cursor()
        # pw 저장(decode된걸로 )
        sql="INSERT INTO account(user_email,user_password) VALUES (%s,%s)"
        curs.execute(sql,(user_email,decode_hash_pw))
        self.order_db.commit()

        curs.close()

    def add_user_info(self,user_email,user_name,user_phonenum):
        curs=self.order_db.cursor()
        sql="INSERT INTO user(user_email,user_name,user_phonenumber) VALUES (%s,%s,%s)"
        curs.execute(sql,(user_email,user_name,user_phonenum))
        self.order_db.commit()

        curs.close()




# 로그인
# account table 조회 
class login(Database):
    def __init__(self):
        super().__init__()

    def compare_data(self,email_text,pw_text):
        # 다시 encode해서 bcrypt의 checkpw함수 사용
        input_pw=pw_text.encode('utf-8')
        curs=self.order_db.cursor(pymysql.cursors.DictCursor)
        sql="SELECT * FROM account WHERE user_email=%s"
        curs.execute(sql,email_text)
        data=curs.fetchone()
        curs.close()
        if not data:
            check_pw=False
        else:
            check_pw=bcrypt.checkpw(input_pw,data['user_password'].encode('utf-8'))
        return check_pw



#주문    
    
class order(Database):
    def __init__(self):
        super().__init__()

    def restaurant_code_exists(self,restaurant_code):
        curs=self.order_db.cursor()
        sql="select * from restaurant where restaurant_code=%s"
        curs.execute(sql,restaurant_code)
        data=curs.fetchone()
        curs.close()
        if data:
            return 1
        else:
            return 0 # 존재하지않으면 0
    
    def minimum_price(self,restaurant_code): # 최소주문금액 조회 
        curs=self.order_db.cursor()
        sql="select * from restaurant where restaurant_code=%s"
        curs.execute(sql,restaurant_code)
        data=curs.fetchone()
        curs.close()

        return data[5]
        
    def show_rest(self): # 음식점코드, 음식점 이름 보여주기 
        curs=self.order_db.cursor()
        #lst=[]
        sql="select * from restaurant"
        curs.execute(sql)
        res_list=curs.fetchall()
       # for x in res_list:
        #    a=[x[0],x[1]]
         #   lst.append(a)
        curs.close()
        return res_list

    def show_menu(self,restaurant_code):
        curs=self.order_db.cursor()
        sql="select * from menu where restaurant_code=%s"
        curs.execute(sql,restaurant_code)
        menu_list=curs.fetchall()

        curs.close()
        return menu_list

    def get_restaurant_name(self,restaurant_code): # 레스토랑 이름 
        curs=self.order_db.cursor()
        sql="select * from restaurant where restaurant_code=%s"
        curs.execute(sql,restaurant_code)
        data=curs.fetchone()
        #res_name=data[1]
        curs.close()
        return data[1]
    # 주문하기 클릭 -> 최소주문 금액 만족하는 check -> ok : ordercode생성 -> order -> order_menu 순서로 등록, 

    def show_menu_list(self,restaurant_code): # checkbox에서 뭐받았는지 체크하게끔 run.py에서
        lst=[]
        curs=self.order_db.cursor()
        sql="select * from menu where restaurant_code=%s"
        curs.execute(sql,restaurant_code)
        data=curs.fetchall()
        curs.close()
        for x in data:
            lst.append(x[2])

        return lst

    def calculate_cost(self,menu,count): #menu, 수량 list로 받음
        curs=self.order_db.cursor()
        cost=[]
        result=0
        for i in range(len(menu)): 
            sql="select * from menu where menu_name=%s"
            curs.execute(sql,menu[i])
            data=curs.fetchone()
            result=data[4]*int(count[i])
            cost.append(result)

        curs.close()
        return cost

    #최소 주문금액 : 금액합치는 건 실행파일에서 하고, 해당 레스토랑 코드의 최소주문금액과 비교
    def compare_minimum_price(self,price,restaurant_code):
        curs=self.order_db.cursor(pymysql.cursors.DictCursor)
        sql="select * from restaurant where restaurant_code= %s"
        curs.execute(sql,restaurant_code)
        data=curs.fetchone()
        if price <data['minimum_order_amount']:
            return 0
        else:
            return 1 # 만족하면 1 반환

    # 주문 코드 생성
    def make_ordercode(self,user_email): #hashlib의 md5 메소드이용
        curs=self.order_db.cursor()
        sql="select * from user where user_email=%s"
        curs.execute(sql,user_email)
        data=curs.fetchone()
        key = md5(data[1].encode('utf8')).hexdigest()
        key=key+str(datetime.now()).replace(':','')[11:-7]
        return key

    def add_order_data(self,order_code,user_email,date,restaurant_code):
        # 여기에 date까지 1 page에서는 4개 칼럼값만 추가
        curs=self.order_db.cursor()
        
        sql="INSERT INTO `order`(order_code,user_email,`date`,restaurant_code) VALUES (%s,%s,%s,%s)"
        curs.execute(sql,(order_code,user_email,date,restaurant_code))
        self.order_db.commit()
        curs.close()

  
    
        
   

    
    def add_order_menu(self,order_code,menu_code,amount,cost): #order menu table에 추가
        curs=self.order_db.cursor()
        
        sql="insert into order_menu(order_code,menu_code,amount,cost) values (%s,%s,%s,%s)"
        curs.execute(sql,(order_code,menu_code,amount,cost))
        self.order_db.commit()
        curs.close()

    def show_coupon_code(self):
        curs=self.order_db.cursor()
        sql="select * from coupon"
        curs.execute(sql)
        data=curs.fetchall()
        curs.close()
        return data

    def get_discount(self,coupon_code):
        curs=self.order_db.cursor()
        sql="select * from coupon where coupon_code=%s"
        curs.execute(sql,coupon_code)
        data=curs.fetchone()
        return data[1]

    def get_menucode(self,menu_lst): # checkbox에서 뭐받았는지 체크하게끔 run.py에서
        lst=[]
        curs=self.order_db.cursor()
        for x in menu_lst:
            sql="select * from menu where menu_name=%s"
            curs.execute(sql,x)
            data=curs.fetchone()
            lst.append(data[0])
        curs.close()

        return lst

    def update_order(self,order_code,address,request,coupon_code):
        curs=self.order_db.cursor()
        sql="update `order` set address= %s, requests=%s,coupon_code=%s where order_code=%s"
        curs.execute(sql,(address,request,coupon_code,order_code))
        self.order_db.commit()
        curs.close()

    def add_payment_data(self,order_code,method,price):
        curs=self.order_db.cursor()
        sql="insert into payment(order_code,payment_method,payment_amount) values (%s,%s,%s)"
        curs.execute(sql,(order_code,method,price))
        self.order_db.commit()
        curs.close()


    


class payment(Database):
    def __init__(self):
        super().__init__()
        
    def get_total(self,order_code):
        curs=self.order_db.cursor()
        sql="select sum(price) from order_menu where order_code=%s"
        curs.execute(sql,order_code)
        total=curs.fetchall()
        print(total)
        return total
        
