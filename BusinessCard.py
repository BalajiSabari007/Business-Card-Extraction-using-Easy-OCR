import pandas as pd
import easyocr
import cv2
import re
import mysql.connector
from PIL import Image
import sqlite3
#--------------------------------------------------------------------------------------------------------------------------------
#mysql.connector.connect(host="127.0.0.1",user="root",password="Sabari@12345",auth_plugin='mysql_native_password',database="plasticmoney")
mydata = sqlite3.connect('plasticmoney')
myfile = mydata.cursor()

Bizcard_table = 'CREATE TABLE IF NOT EXISTS Bizcard (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Designation TEXT, Company_name TEXT, Address TEXT, Contact_number TEXT, Email_id TEXT, Web_link TEXT, Image BLOB);'
myfile.execute(Bizcard_table)
#---------------------------------------------------------------------------------------------------------------------------------
reader = easyocr.Reader(["en"])
def load_dataset(img):
    ans = reader.readtext(img, paragraph=True)
    data = []
    k = 0 
    for i in ans:
        data.append(ans[k][1])
        k =+ 1
    data
    card =" ".join(data)
    
#--------------------------------------------------------------Adding phone Number-------------------------------------------------
    phone_num = re.compile(r'\+*\d{2,3}-\d{3,10}-\d{3,10}')
    ph_number = ""

    for j in phone_num.findall(card):
        ph_number = ph_number + ' ' +  j
        card = card.replace(j, "")

#------------------------------------------------------------Adding Weblink------------------------------------------------------------
    web_link = re.compile(r'www.?[\w.]+')
    web = ""

    for l in web_link.findall(card):
        web = web + l
        card = card.replace(l, "")

#-----------------------------------------------------Adding Email ID-------------------------------------------------------------------
    email_id = re.compile(r'([a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+)')
    email = ""

    for m in email_id.findall(card):
        email = email + m
        card = card.replace(m, "")

#-----------------------------------------------------------Adding address------------------------------------------------------------------------
    address = re.compile(r'\d{2,3}.+\d{6}')
    add = ""

    for n in address.findall(card):
        add += n
        card = card.replace(n, "")

#-------------------------------------------------------Seperating Designation----------------------------------------------------------------------
    post_name = ['DATA MANAGER', 'CEO & FOUNDER','General Manager', 'Marketing Executive', 'Technical Manager']
    designation = ''
    for f in post_name:
        if re.search(f, card):
            designation += f
            card = card.replace(f, '')

#----------------------------------------------------------- Seperating the company name------------------------------------------------------------
    company_name = ['selva digitals','GLOBAL INSURANCE','BORCELLE AIRLINES','Family Restaurant','Sun Electricals']
    company = ""

    for d in company_name:
        if re.search(d, card):
           company += d
           card = card.replace(d, "")

    name = card.strip()
#-------------------------------------------------------Reading and getting byte values of image-----------------------------------------------------

    with open(img, 'rb') as file:
        data = file.read()

#---------------------------------------------------------------------------------------------------------------------------------------------------
    Bizcard_insert = 'INSERT INTO Bizcard (Name, Designation, Company_name, Address, Contact_number, Email_id, Web_link, Image) VALUES (?,?,?,?,?,?,?,?);'
    myfile.execute(Bizcard_insert, (name, designation, company, add, ph_number, email, web, data))

#---------------------------------------------------------------------------------------------------------------------------------------------------
def extract_data(img):
    reader = easyocr.Reader(["en"])
    ans = reader.readtext(img, paragraph=True)
    image = cv2.imread(img)
    for docs in ans:
        top_left = tuple([int(val) for val in docs[0][0]])
        bottom_right = tuple([int(val) for val in docs[0][2]])
        txt = docs[1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.rectangle(image, top_left, bottom_right, (255,215, 0), 5)
        img = cv2.putText(image, txt, top_left, font, 0.8, (0, 0, 139), 2, cv2.LINE_AA)
    
    return img

def show_dataset():
    new_data = pd.read_sql("SELECT * FROM Bizcard")
    return new_data

#----------------------------------------------------------------End--------------------------------------------------------------------