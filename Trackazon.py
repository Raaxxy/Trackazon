from bs4 import BeautifulSoup
import requests
import urllib.request
import smtplib
import time

prices_list = []

def check_price():
    url = 'https://www.amazon.in/gp/product/B08498H13H/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1'
    page = requests.get(url ,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"})#for not getting captcha
    soup = BeautifulSoup(page.text, 'html.parser')#using bs4 to parse...
    product_price = soup.find(class_ = "a-price-whole")#find the class in which price is located 
    print(product_price.text)#prints the current price
    product_price = float(product_price.replace(",", "").replace("₹", ""))
    prices_list.append(product_price)
    return product_price

def send_email(message, sender_email, sender_password, receiver_email):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, sender_password)#add sender's email and sender's password for smtp to login
    s.sendmail(sender_email, receiver_email, message)#add sender's email,reveiver's email and message which you want to send
    s.quit()

def price_decrease_check(price_list):
    if prices_list[-1] < prices_list[-2]:
        return True
    else:
        return False

count = 1
while True:
    if count > 1:
        flag = price_decrease_check(prices_list)
        if flag:
            decrease = prices_list[-1] - prices_list[-2]
            message = f"The price has decreased!! Please check the item. The price decreased by {decrease} rupees."
            send_email(message, sender_email, sender_password, receiver_email) #ADD THE OTHER AGRUMENTS sender_email, sender_password, receiver_email
    print("working")
    time.sleep(43000)#will check again in 6 hrs whether the price has changed or not 
    count += 1