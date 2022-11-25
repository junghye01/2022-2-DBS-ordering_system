import pymysql
import bcrypt

class Database(object):
    def __init__(self):
        self.order_db=pymysql.connect(
            user='root',
            password='@hyungsuk1234',
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
    #... 회원가입할 때 user, account table에 모두 저장
    def add_email_data(self,user_email):
        curs=self.order_db.cursor()
        sql="INSERT INTO user(user_email) VALUES (%s)"
        curs.execute(sql,user_email)
        self.order_db.commit()
        
        curs=self.order_db.cursor()
        sql='INSERT INTO account(user_email) VALUES (%s)'
        curs.execute(sql,user_email)
        self.order_db.commit()

        curs.close()

    def add_password(self,user_email,user_password):
        new_salt=bcrypt.gensalt()
        new_pw=user_password.encode('utf-8')
        hashed_pw=bcrypt.hashpw(new_pw,new_salt)# 해시된 비밀번호
        decode_hash_pw=hashed_pw.decode('utf-8')

        curs=self.order_db.cursor()
        # pw 저장(decode된걸로 )
        sql="UPDATE account set user_password=%s WHERE user_email=%s "
        curs.execute(sql,(decode_hash_pw,user_email))
        self.order_db.commit()

        curs.close()

    def add_user_info(self,user_email,user_name,user_phonenum):
        curs=self.order_db.cursor()
        sql="UPDATE user SET user_name=%s where user_email=%s"
        curs.execute(sql,(user_name,user_email))
        self.order_db.commit()

        curs=self.order_db.cursor()
        sql="UPDATE user SET user_phonenumber=%s where user_email=%s"
        curs.execute(sql,(user_phonenum,user_email))
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
        check_pw=bcrypt.checkpw(input_pw,data['user_password'].encode('utf-8'))
        return check_pw



#주문    
    
class order(Database):
    def __init__(self):
        super().__init__()
        
    def show_rest(self): # 1. 음식점 보여줌
        curs=self.order_db.cursor()
        sql="select * from restaurant;"
        curs.execute(sql)
        res_list=curs.fetchall()
        return res_list
        
    
    def add_order_menu(self,order_code,restaurant_code,menu_code,amount,cost):
        curs=self.order_db.cursor()
        sql="isnert into `order`(order_code) values(%s);"
        curs.execute(sql,order_code) #먼저 order 엔티티에 order_code 입력
        self.order_db.commit()
        
        sql="insert into order_menu values (%s,%s,%s,%s,%s);"
        curs.execute(sql,order_code,restaurant_code,menu_code,amount,cost) 
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
        