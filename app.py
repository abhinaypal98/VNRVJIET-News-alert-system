# Vnr news updates through email at scheduled time 
# Sender email should be google account(<user>@gmail.com)
import smtplib
from email.message import EmailMessage
import os
from datetime import datetime
from dateutil.tz import gettz
from datetime import date
now = datetime.now(tz=gettz('Asia/Kolkata'))
current_time = now.strftime("%H:%M:%S")
today = date.today()
current_day = today.strftime("%d/%m/%y")
User_name =os.getenv("User_name")  # Give gmail id through which you are sending emails
Password = os.getenv("Password")   # unique password for the user

# Making a Request for vnrvjiet news site and extracting only news from site normal news
def Request_news():
    import requests
    from bs4 import BeautifulSoup as BS
    page = requests.get("http://www.vnrvjiet.ac.in/")
    contents = BS(page.content.decode(),"html.parser")
    News = contents.find('marquee').find_all('a')
    data =[]
    for x in News:
        contents = x.contents[1:-1]
        link = x.get('href').strip()
        if("/" not in link):
            link = "http://www.vnrvjiet.ac.in/"+link
        if(len(contents) == 1):
            img_link = 'No'
        else:
            img_link ="http://www.vnrvjiet.ac.in/"+contents[0].get('src')
        news = contents[-1].contents[0].strip()
        data.append((link,img_link,news))
    return data

# Making a Request for vnrvjiet news site and extracting only news from site exam news
def EXAM_NEWS():
    import requests
    from bs4 import BeautifulSoup as BS
    connection = requests.get("http://www.vnrvjiet.ac.in/vnrexams.php")
    page = BS(connection.content.decode(),'html.parser')
    k = page.find('div','single_post_content')
    Data = k.find_all('a')
    data = []
    for x in Data:
        link = x.get_attribute_list('href')[0].strip()
        if('/' not in link):
            link = 'http://www.vnrvjiet.ac.in/'+link
        button = x.find('button')
        button_contents =button.contents[-2:]
        if(len(button_contents) == 2):
            image_link = 'http://www.vnrvjiet.ac.in/'+button_contents[0].get_attribute_list('src')[0]
        else:
            image_link = 'No'
        news = button_contents[-1].strip()
        data.append((link,image_link,news))
    return data
    

# construct email format
email = EmailMessage()
email['Subject'] = f' VNRVJIET NEWS - Date : {current_day}   Time : {current_time}'
email['From'] = User_name
email['To'] = "braviteja2910@gmail.com"   # sender email, use list if there are more than one emails. Any email id is accepted


contents ="<body><h1> VNRVJIET LATEST NEWS </h1><br>"
data1 = Request_news()
for x,y,z in data1:
    if('No' not in y):
        contents+=f'<br><h4> <img src ="{str(y)}">  {z} <a href = "{str(x)}">..(more)</a><br><h4>'
    else:
        contents+=f'<br><h4>{z} <a href = "{str(x)}">..(more)</a><br><h4>'
        
contents+="<br><br><br><h1> VNRVJIET EXAMINATION NEWS </h1><br>"
data = EXAM_NEWS()
for x,y,z in data:
    if('No' not in y):
        contents+=f'<br><h4> <img src ="{str(y)}">  {z} <a href = "{str(x)}">..(more)</a><br><h4>'
    else:
        contents+=f'<br><h4>{z} <a href = "{str(x)}">..(more)</a><br><h4>'


contents+="</body>"


email.set_content(contents, subtype='html')


# Send the message via local SMTP server.

with smtplib.SMTP('smtp.gmail.com',587) as s:
    s.starttls()
    s.login(User_name,Password)
    s.send_message(email)
