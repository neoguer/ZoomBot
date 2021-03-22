from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import pyperclip
import time
import smtplib, ssl
import datetime

### ENTER EMAILS HERE:
emails = []

chrome_options = Options()
chrome_options.add_argument("--kiosk")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
drive = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
drive.get('')

initial = 0

### AFTER CHROMEDRVIER STARTS, JOIN THE MEETING ON BROWSER, SOLVE THE RECAPTCHA,
input('Solve reCaptcha and join meeting')


def getnumber(pagehtml):
    html1 = pagehtml.replace(pagehtml[:pagehtml.find('number-counter')],'')
    html2 = html1.replace(html1[html1.find('"footer-button__button-label">Participants'):],'')
    html3 = html2.replace(html2[:html2.find('<span>') + 6],"")
    html4 = html3.replace(html3[html3.find('</span>'):],'')
    number = int(html4)
    return number

def getparticipants(pagehtml):
    html1 = pagehtml.replace(pagehtml[:pagehtml.find('participants-ul')],'')
    html2 = html1.replace(html1[html1.find('scrollbar-track'):],'')
    html3 = html2.split('aria-label="')
    html3 = html3[1:]
    for i in range(len(html3)):
        html3[i] = html3[i].replace(html3[i][html3[i].find('  '):],'')
    participantslist = html3
    return participantslist

def notify(participants, emails):
    sender = ""
    receiver = emails
    password = ""
    SUBJECT = 'New Zoom Participants! [' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +']'

    TEXT = 'Hi Gomblock member!\n\nYour Zoom meeting has new participants:\n'
    for i in participants:
        TEXT = TEXT + i + '\n'

    TEXT = TEXT + '\nSee you soon!\n-Automated Zoom Bot'
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sender,password)
    server.sendmail(sender,receiver,message)
    print('Email sent at:',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    

pagehtml = str(drive.page_source)
initial = getnumber(pagehtml)

n = 0
while(n==0):
    time.sleep(30)
    pagehtml = str(drive.page_source)
    number = getnumber(pagehtml)
    if (number < initial):
        initial = number
    if (number > initial):
        participantslist = getparticipants(pagehtml)
        notify(participantslist,emails)
        initial = number