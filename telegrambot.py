#PyBank telegram bot
import pymysql
from prettytable import PrettyTable
import smtplib
from email.mime.text import MIMEText
from datetime import date
import time
import random

from typing import Final
from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes,ConversationHandler, CallbackContext
conn = pymysql.connect(host = 'localhost',user = 'root',password = '',database = '')

c = conn.cursor()

s = '''
𝑷𝒚𝑩𝒂𝒏𝒌 - 𝑫𝒊𝒓𝒆𝒄𝒕𝒆𝒅 𝒃𝒚 𝑷𝒓𝒊𝒚𝒂𝒎 𝑱𝒂𝒊𝒏

Welcome! Perform transactions:

Please follow the format below to perform any transaction:-

format:𝐓,𝐍𝐍,𝐏𝐏𝐏𝐏,𝐌𝐌𝐌𝐌
example:2,20,123,100 

T    = Type of command(check = 1,deposit = 2 or withdraw = 3)
NN   = Your Account num
PPPP = Your Account Password
MMMM = Amt of money(optional)
(MMMM only for withdrawl and deposit)

FOR
𝟏. 𝐂𝐡𝐞𝐜𝐤 𝐀𝐜𝐜𝐨𝐮𝐧𝐭:
   Type:𝟏, 𝐀𝐜𝐜𝐍𝐮𝐦, 𝐏𝐚𝐬𝐬
   Ex: 1, 20, 123
   Shows account info.

𝟐. 𝐃𝐞𝐩𝐨𝐬𝐢𝐭 𝐌𝐨𝐧𝐞𝐲:
   Type: 𝟮, 𝐀𝐜𝐜𝐍𝐮𝐦, 𝐏𝐚𝐬𝐬, 𝐀𝐦𝐭
   Ex: 2, 20, 123, 100
   Adds 100 units.

𝟑. 𝐖𝐢𝐭𝐡𝐝𝐫𝐚𝐰 𝐌𝐨𝐧𝐞𝐲:
   Type: 𝟑, 𝐀𝐜𝐜𝐍𝐮𝐦, 𝐏𝐚𝐬𝐬, 𝐀𝐦𝐭
   Ex: 3, 20, 123, 50
   Takes out 50 units.

Abbreviations:
- AccNum: Account number.
- Pass: Account password.
- Amt: Amount.

E.g., check account(FOR TRIAL): 1, 20, 123

'''
h = """PyBank - Directed by Priyam Jain

Welcome to PyBank! This program allows you to perform various financial transactions easily. Here's a breakdown of the available options:

1. Check Account:
To view your account details, simply type "1" followed by your account number and password, like this: 1, YourAccountNumber, YourPassword. For example: 1, 20, 123. This will display your account information on the screen.

2. Deposit Money:
To add funds to your account, use the command "2" along with your account number, password, and the amount you want to deposit, like this: 2, YourAccountNumber, YourPassword, AmountToAdd. For example: 2, 20, 123, 100. This will increase your account balance by the specified amount.

3. Withdraw Money:
If you need to take money out of your account, use the "3" command along with your account number, password, and the amount you wish to withdraw, like this: 3, YourAccountNumber, YourPassword, AmountToWithdraw. For instance: 3, 20, 123, 50. This will reduce your account balance by the specified amount.

Please note the following abbreviations:
- AccNum: Account number
- Pass: Account password
- Amt: Amount of money

Feel free to try out these commands! For example, you can check your account details by typing: 1, 20, 123.
"""


TOKEN: Final = 'TOKEN'
bot_username:Final = 'USERNAME'

async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(s)
    
async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(h)
    
async def custom_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('chalo')
    
async def menu_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(s)

def handel_response(text:str)->str:
    n = text.lower()
    if 'hello' in n:
        return 'hello bro'
    if "," in n:
        l = text.split(",")
        if len(l)>=3 and len(l)<=4:
            v = res(l)
            return v
        else:
            return 'Please Provide Sufficient info'
    return 'i dont understand'




async def handel_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    msg_type:str = update.message.chat.type
    text:str = update.message.text
    print(f'User({update.message.chat.id})in {msg_type}:"{text}"')

    if msg_type == 'group':
          if bot_username in text:
             new_text:str = text.replace(bot_username,'').strip()
             response = handel_response(new_text)
          else:
              return
    else:
        response:str = handel_response(text)
        print('Bot:',response)
        await update.message.reply_text(response)
async def error(update:Update,context:ContextTypes.DEFAULT_TYPE):
        print(f'Update{update}caused error{context.error}')

def main():
    app = Application.builder().token(TOKEN).build()
    print("Starting Bot...")
    #command
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))
    app.add_handler(CommandHandler('menu',menu_command))

    
    #messages
    app.add_handler(MessageHandler(filters.TEXT,handel_message))
    #error
    app.add_error_handler(error)
    #to check constatly for update
    print("Polling...")
    app.run_polling(poll_interval = 3)
    
def res(l):
    #l = [transaction,ano,password,money]
    tran = int(l[0])
    if tran == 1:
        #require = ano,password(int)
        s = checking_account(l[1],l[2])
        return s
    
    elif tran == 2:
        #require = ano,password,money
        s = deposit_money(l[1],l[2],l[3])
        return s
    
    elif tran == 3:
        #require = ano,password,money
        s = withdraw_money(l[1],l[2],l[3]) 
        return s
    
    else:
        return "Command cannot be interprented please try again"
    
def checking_account(ano,password):
   
    query = "select * from sbank where sno = {} and password = {}".format(ano,password)
    c.execute(query)
    
    data = c.fetchone()
    if len(data) != 0:
       ano = data[0]
       name = data[1]
       money = data[2]
       password = data[3]
       gmail = data[4]
       s =" Checking Account:-\n\n Account no:"+str(ano)+"\n Name:"+name+"\n Money:"+str(money)+"\n password:"+str(password)+"\n Gmail:"+str(gmail)+" \n\n Thank You"

       return s


   
    
def deposit_money(ano,password,depo):
    
    query = "select * from sbank where sno = {} and password = {}".format(ano,password)
    c.execute(query)
    data = c.fetchone()
    ano = data[0]
    name = data[1]
    money = data[2]
    gmail = data[4]
    total_money = money+int(depo)
    
    query = "Update sbank set money = {} where sno = {}".format(total_money,ano)
    c.execute(query)
    conn.commit()

    query = "select money from sbank where sno = {} and password = {}".format(ano,password)
    c.execute(query)
    data = c.fetchone()
    if data[0] == total_money:
        s = " Deposit Money\n "+str(depo)+" rupees Succesfully deposited in \nAccount no: "+str(ano)
        l = [ano,name,gmail,depo]
        fgm(l,3)
    return s
    
def withdraw_money(ano,password,draw):
    s = "with_drawmoney"
    query = "select * from sbank where sno = {} and password = {}".format(ano,password)
    c.execute(query)
    data = c.fetchone()
    ano = data[0]
    name = data[1]
    money = data[2]
    gmail = data[4]
    if int(draw)>money:
        return "You Dont Have Enough Balance to WithDraw Money"
    total_money = money+int(draw)
    
    query = "Update sbank set money = {} where sno = {}".format(total_money,ano)
    c.execute(query)
    conn.commit()

    query = "select money from sbank where sno = {} and password = {}".format(ano,password)
    c.execute(query)
    data = c.fetchone()
    if data[0] == total_money:
        s = " WithDrawn Money\n "+str(draw)+" rupees Succesfully withdrawn from \nAccount no: "+str(ano)
        l = [ano,name,gmail,draw]
        fgm(l,4)
    return s
    
#________________________________________________________________________________________________________________________________________________        
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
         
        
       
    
    sender = "SENDER"
    recipients = ["SENDER",gm]
    password = "PASSWORD"
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
   
   
    
main()    
           

