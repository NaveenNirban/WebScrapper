import requests
from bs4 import BeautifulSoup
import smtplib
import time
import base64
fpass=open("pass_log.txt","rb")
fuser=open("user_log.txt","rb")
user_read=fuser.read()
pass_read = fpass.read()
pass1=base64.b64decode(pass_read)
password=pass1.decode("utf-8")
user1=base64.b64decode(user_read)
username=user1.decode("utf-8")
fuser.close
fpass.close
print(password)
URL=input("Enter product URL = ")
our_price=input("Enter Choice price = ")
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
def price_checker():
    page=requests.get(URL,headers=headers)
    soup=BeautifulSoup(page.content,"html.parser")
    title=soup.find(id="productTitle").get_text()
    try:
       price=soup.find(id="priceblock_dealprice").get_text()
    except AttributeError:
       print("No current deals on this product, Checking for any sales")
       try:
          price=soup.find(id="priceblock_saleprice").get_text()
       except AttributeError:
          print("No sales found, regular price is ")
          price=soup.find(id="priceblock_ourprice").get_text()
    converted_price=price[2:8]
    if(converted_price<our_price):
        send_mail()
        print("Congratulations!!!\nCurrent price = ",converted_price)
    else:
        print("Sorry!!!\nCurrent price is = ",converted_price)
        print("Checking again in next 1 hour")
def send_mail():
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password)
    fuser.close()
    fpass.close()
    subject = "Price are very low check it out"
    body = "Check it out link = https://www.amazon.in/Power-your-Subconscious-Mind/dp/8194058678/ref=tmm_hrd_swatch_0?_encoding=UTF8&qid=1566980009&sr=8-1-spons"
    msg = f"subject:{subject}\n\n{body}"
    server.sendmail(username,"your email",msg)
    print('HEY MAIL HAS BEEN SENT!!!\n Another mail will be on to you next in 1 hour.')
    server.quit()
while(True):
    price_checker()
    time.sleep(60*60)
