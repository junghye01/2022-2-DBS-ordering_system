from database import (Database,login,signup,order,payment)
from user import User,order_menu
from restaurant import Restaruant

class Menu:
    def __init__(self):
        self.email=''
        self.phone_number=''
        self.name=''
        self.pw=''
        self.selection=1
        
        

    def login_sign_menu(self,userselection):
        
        if userselection==1: #login
            self.email=input('이메일 입력(필수):')
            self.pw=input('비밀번호 입력(필수):')
            login_result=login().compare_data(self.email,self.pw)
            if login_result==1:
                print('로그인 성공')
                User.email=self.email
                User.pw=self.pw
                User.name=Database().load_user_name(self.email)
                User.phone_number=Database().load_user_phonenum(self.email)
                return True
            else: 
                print('존재하지 않는 이메일 또는 비밀번호입니다')
                return False
    

        elif userselection==2: #signup
            self.name=input('이름 입력(필수):')
            self.email=input('이메일 입력(필수)')
            self.pw=input('비밀번호 입력:')
            self.phone_number=input('전화번호 입력: ')
            
            if Database().email_not_exists(self.email): # 회원가입 가능
                print('사용할 수 있는 이메일입니다')
                signup().add_email_data(self.email)
                signup().add_password(self.email,self.pw)
                signup().add_user_info(self.email,self.name,self.phone_number)

                User.name=self.name
                User.email=self.email
                User.pw=self.pw
                User.phone_number=self.phone_number
                print('회원가입 성공')

                return True
            else:
                print('존재하는 이메일입니다')
                return False

    def load_user_data(self):
        print('##로그인 정보##\n')
        user_dict={}
        user_dict['name']=User.name
        user_dict['email']=User.email
        user_dict['phone_number']=User.phone_number

        for key in user_dict.keys():
            print(key,':',user_dict[key])
    
    #내가 따로 추가했어!!        
    def load_user_email(self):
        return User.email
            
    
class Rest_menu:
    def __init__(self):
        self.restaurant_code=''
        self.restaurant_name=''
        self.restaurant_location=''
        self.restaurant_phonenumber=''
        self.business_hours=''
        self.minimum_order_amount=''
        
    def show_menu(self, selection):
        self.show_res()
           
class Order_table:
    def __init__(self):
        self.order_code=''
        self.email=''
        self.date=''
        self.address=''
        self.request=''
        self.restaurant=''
        self.coupon_code=''
        self.payment=''
        self.total_price=''
     
    #주문 마지막 단계    
    def order_table(self,order_code,res_code):
        self.order_code=order_code      
        print("주문코드: "+self.order_code)
        #메인문에서 로그인 후에 이메일정보를 계속 유지
        self.email=Menu().load_user_email()
        print("이메일: "+self.email)
        print("날짜 ")#어떻게 가져올지 생각중
        self.address = input("주소: ")
        self.request=input("요청사항:")
        self.restaurant=res_code
        print("식당코드: "+self.restaurant)
        self.payment=input("결제방식: ")
        self.coupon_code=input("쿠폰코드: ")
        self.total_price=payment().get_total(self.order_code)
        print("총 가격: "+str(self.total_price))
        return True