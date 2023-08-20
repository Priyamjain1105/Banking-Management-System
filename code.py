#small bank
#deposit withdraw
import pymysql
from prettytable import PrettyTable
import smtplib
from email.mime.text import MIMEText
from datetime import date
import time
import random

conn = pymysql.connect(host = 'localhost',user = 'root',password = 'arunrockstar',database = 'l')

c = conn.cursor()
#[account_no,name,money,password]
def deco():
    print("\n_______________________________________________\n")

def main():
    print("Press 1 for Client")
    print("Press 2 for managing staff")
    ch = int(input("Enter Your Chooise:"))
    deco()
    if ch == 1:
        client()
    elif ch == 2:
        managing_staff()
    else:
        main()
        deco()
    
    
def client():
    print("Press 1 For Login")
    print("Press 2 for Register new account")
    ch = int(input("Please Enter Your Chooise"))
    if ch == 1:
        login()
    elif ch == 2:
        print("\n REGISTRATION \n")
        new_account()
        
def login():
    t = check()
    p = show_account(t[0],t[1])
    while True:
          deco()
          print("Hello ",p[1], "What can we do for you \n")
          print("Press 1 for Deposit")
          print("Press 2 for Withdraw")
          print("Press 3 for Checking Your Account")
          print("Press 4 Transfer the money")
          ch = int(input("Enter your chooise"))
          deco()
          if ch == 1:
             deposit(t[0],t[1])
          elif ch == 2:
             withdraw(t[0],t[1])
          elif ch == 3:
             show_account(t[0],t[1],2)
          elif ch == 4:
             transfer()
          else:
             print("Please enter the right chooise")
             main()
             break;
    
    
#___________________________________________________________________________________________________________________________________
def new_account():
    fname = input("Enter Your First Name:")
    lname = input("Enter Your Last Name:")
    name = fname+" "+lname
    c.execute("select max(sno) from sbank")
    #((1))
    data  = c.fetchall()
    sno = data[0][0]+1
    s = int(sno)
    while True:
        gmail = input("Enter Your Gmail:")
        rand = random.randint(1000, 9999)
        pc = fname[0]+lname[0]+fname[1]+lname[1]+str(s)+str(rand)
        fgm([0,name,gmail,pc],2)
        passcode = input("Enter The passcode sended to you gmail:")
        if passcode == pc:
            print("Gmail Verified succesfully")
            break;
        else:
            print("Wrong passcode please try again")
            
    print("Your Account Num is:",sno)
    password = input("Create Your Password(in number):")
    print("Making your account please wait...")
    
   
    money = 10
    
    query = "insert into sbank values({},'{}',{},{},'{}')".format(s,name,money,password,gmail)
    #print(query)
    c.execute(query)
    conn.commit()
    
    print("Your Account Created Succesfully")
    show_account(s,password,2)
    fgm([s,name,gmail,password],t=1)
    
    
def deposit(account,password):
    p = show_account(account,password)
    print(p)
    query = "select * from sbank where sno = {}".format(account)
    depo = int(input("Enter the amount of money you want to deposit:"))
    print("Please wait transaction in progress...")
    total_money = p[2]+depo
    query = "Update sbank set money = {} where sno = {}".format(total_money,account)
    c.execute(query)
    conn.commit()
    
    #show_account(account,password,2)
    a = show_account(account,password,1)
    name = a[1]
    gmail = a[4]
    fgm([account,name,gmail,depo],3)
    print("Transaction succesful")
    
    
    
    
    
def withdraw(account,password):
    
    p = show_account(account,password)
    ano = p[0]
    total_money = p[2]
    
    
    withdraw_money = int(input("Enter the amount of money you want to cash:"))
    print("Please wait transaction is in progress...")
    if withdraw_money <= total_money:
       money_left = total_money - withdraw_money
       c.execute("update sbank set money = {} where sno = {}".format(money_left,ano))
       conn.commit()
       
      
       #show_account(t[0],t[1],2)
       a = show_account(account,password,1)       
       
       name = a[1]
       gmail = a[4]
       fgm([account,name,gmail,withdraw_money],4)
       
       print("Transaction succesful")
       
    else:
        print("Not Enough Balance")
    
    

def check():
    deco()
    flag = True
    while flag:
         account = int(input("Account Num:"))

         #checking presence of account num
         c.execute("select sno from sbank;")
         data = c.fetchall()
         #print(data)
         
         for i in data:
             if i[0] == account:
                #checking password
                password = int(input("password:"))
                query = "select password from sbank where sno = {}".format(account)
                c.execute(query)
                data = c.fetchone()
                if data[0] == password:
                   flag = False
                   return account,password
                   deco()
                else:
                       print("WRONG PASSWORD")
                       deco()
    
     

def show_account(sno,password,t = 1):
    query = "select * from sbank where sno = {} and password = {}".format(sno,password)
    c.execute(query)
    if t == 1:
       data = c.fetchone()
       return data
    elif t ==2:
         data = c.fetchall()
         ptable(data)
        
def transfer():
    print("This Feature is not yet available")

    
    
    
    
def managing_staff():
    print("Press 1 to see all accounts")
    print("Press 2 to type a sql command on selecting")
    ch = int(input("Enter Your Chooise"))
    if ch == 1:
        show_all_accounts()
    elif ch == 2:
        while True:
              deco()
              command = input("Enter command:")
              c.execute(command)
              data = c.fetchall()
              ptable(data)


def show_all_accounts():
    query = "SELECT * FROM sbank;"
    c.execute(query)
    result = c.fetchall()
    ptable(result)
    
    
    
def ptable(result):
    table = PrettyTable()
    table.field_names = [col[0] for col in c.description]
    for row in result:
        table.add_row(row)
    print(table)

def datetime(t = 1):
    if t == 1:
        today = date.today()
        d2 = today.strftime("%B %d, %Y")
        return d2
    elif t == 2:
         o = time.localtime()
         ct = time.strftime("%H:%M:%S", o)
         return ct
    
#____________________________________________________________________________________________________________________________________________________
#l =[ano,name,gm,message,money,transfertype,date,time]
def fgm(l,t = 1):
    subject = "| PyBANK |"
    #body
    ano = l[0]
    name = l[1]
    gm = l[2]
    
    if t == 1:
       print("Thankyou")
       body = "You succesfully created your new account"+name+"! \n\n Your Account No is:"+str(ano)+"\n Your Password is:"+str(l[3])
    elif t == 2:
        print("Checking Gmail")
        body = "Hello "+name+" \n\n Your Passcode  is:"+str(l[3])
        
    elif t == 3:
         print("Money Deposit")
         query = "select money,gmail from sbank where sno = {}".format(ano)
         deposit = l[3]
         c.execute(query)
         data = c.fetchone()
         money = data[0]
         gm = data[1]
         print(money,gm)
         body = "Hey "+name+","+str(deposit)+" Rupees deposited in your back account \n\n Account no:"+str(ano)+"\n Your Current Balance is "+str(money)+" Rupees only"
         
    elif t == 4:
         print("Money Withdrawn")
         query = "select money,gmail from sbank where sno = {}".format(ano)
         withdrawn = l[3]
         c.execute(query)
         data = c.fetchone()
         money = data[0]
         gm = data[1]
         print(money,gm)
         body = "Hey "+name+","+str(withdrawn)+" Rupees withdrawn from your back account \n\n Account no:"+str(ano)+"\n Your Current Balance is "+str(money)+" Rupees only"
         
        
       
    
    sender = "priyam.automatedmails@gmail.com"
    recipients = ["priyam.automatedmails@gmail.com",gm]
    password = "ujewklzxlhtovdoq"
    send_email(subject, body, sender, recipients, password)
     




def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()    

    
