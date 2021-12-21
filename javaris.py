import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import PyPDF2

import pyttsx3 #provide engine -- convert text to voice
import speech_recognition as sr #to take command for user
import datetime
import os
import cv2
import random
from requests import get
import requests
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import pyjokes
import pyautogui

engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)#voices[0] = male or female voice of javaris

#fnction to convert text to audio
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

#to take input from user
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening ....")
        r.pause_threshold = 1 #if user stops while speaking javaris doenot shutdown
        audio = r.listen(source,timeout=1000,phrase_time_limit=5)
    try:
        print("Recognized")
        query = r.recognize_google(audio,language='en-in')
        print(f"user said : {query}")

    except Exception as e:
        speak("Say that again please...")
        return "none"
    return query

#fow greeting good morning or afternoon
def wish():
    hour = int(datetime.datetime.now().hour)
    t = datetime.datetime.now()

    if hour >=0 and hour<12:
        speak(f"Good morning, it's {t}")
    elif hour>12 and hour<18:
        speak(f"Good afternoon, it's {t}")
    else:
        speak(f"Good evening, it's {t}")
    speak("I am jarvis, please tell me how can i help you")

def sendEmail(to,content):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login("bhavyasehgal4241@gmail.com","Gndu#4241")
    server.sendmail("bhavyasehgal4241@gmail.com",to,content)
    server.close()

def news():
    main_url = "https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=e06a6bc62fc94c90a6c3f0baf6628e3e"
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first","second","third","fourth","fifth","sixth","seventh","eight","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")

def pdf_reader():
    book = open("",'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"Total number of pages in this book {pages}")
    speak("enter the page that I have to read")
    pg = int(input("please enter page number: "))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)



if __name__ == '__main__':#to run it in this program only and not in any other
    #takecommand()
    wish()
    while True:
        if 1:
            query = takecommand().lower()

            #logic building for tasks

            if "open notepad" in query:
                npath = "C:\\WINDOWS\\system32\\notepad.exe"
                os.startfile(npath)
            elif "open command prompt" in query:
                os.system('start cmd')
            elif "open camera" in query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam',img)
                    k=cv2.waitKey(50)
                    if k == 27:
                        break
                    cap.release()
                    cv2.destroyAllWindows()
            elif "play music" in query:
                music_dir = "D:\\bhavya\\Music"
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir,songs[0]))
            elif "ip address" in query:
                ip = get('https://api.ipify.org').text
                speak(f"your IP address is {ip}")
            elif "wikipedia" in query:
                speak("searching wikipedia...")
                query = query.replace("wikipedia","")
                result = wikipedia.summary(query, sentences = 2)
                speak("According to wikipedia")
                speak(result)
                #print(result)
            elif "open youtube" in query:
                webbrowser.open("www.youtube.com")
            elif "open stack overflow" in query:
                webbrowser.open("www.stackoverflow.com")
            elif "open instagram" in query:
                webbrowser.open("www.instagram.com")
            elif "open google" in query:
                speak("What should I search on google")
                cm = takecommand().lower()
                webbrowser.open(f"{cm}")
            elif "send message" in query:
                kit.sendwhatmsg('+916283447051',"this is testing protocol",2,25)
            elif "play song on youtube" in query:
                kit.playonyt("Kasoor")
            elif "send email" in query:
                speak("what should I  send")
                content = takecommand().lower()
                if "send a file" in content:
                    email = "bhavyasehgal4241@gmail.com"
                    password = "Gndu#4241"
                    send_to_mail = "bhavyasehgal4241@gmail.com"
                    speak("what should be subject od mail")
                    query1 = takecommand().lower()
                    subject = query1
                    speak("what is message of mail")
                    query2 = takecommand().lower()
                    message = query2
                    speak("please enter the correct path of file here")
                    file_location = input("please enter the file path here: ")
                    speak("please wait i'm sending the mail")
                    msg = MIMEMultipart()
                    msg['From'] = email
                    msg['To'] = send_to_mail
                    msg['Subject'] = subject

                    msg.attach(MIMEText(message,'plain'))

                    #setup attachement
                    filename = os.path.basename(file_location)
                    attachment = open(file_location,"rb")
                    part = MIMEBase('application','octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition','attachment;filename = %s'%filename)
                    msg.attach(part)

                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login("bhavyasehgal4241@gmail.com", "Gndu#4241")
                    text = msg.as_string()
                    server.sendmail("bhavyasehgal4241@gmail.com", send_to_mail, text)
                    server.quit()
                    speak("Email sent")
                else:
                    try:
                        to = "bhavy.ebox@gmail.com"
                        sendEmail(to,content)
                        speak("Email sent")
                    except Exception as e:
                        print(e)
                        speak("Not able to send Email")
            #to close application
            elif "close notepad" in query:
                speak("okay, closing notepad")
                os.system("taskkill /f /im notepad.exe")
            #to set alarm
            elif "set alarm" in query:
                nn = int(datetime.datetime.now().hour)
                if nn == 22:
                    music_dir = "D:\\bhavya\\Music"
                    songs = os.listdir(music_dir)
                    os.startfile(os.path.join(music_dir, songs[0]))
            #to tell joke
            elif "tell a joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)
            elif "shut down the system" in query:
                os.system("shutdown /s /t 5")
            elif "restart the system" in query:
                os.system("shutdown /r /t 5")
            elif "sleep the system" in query:
                os.system("rundll32.exe powrprof.dll, SetSuspendtate 0,1,0")
            elif "tell me news" in query:
                speak("please wait,fetching the latest news")
                news()
            elif "switch the window" in query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")
            #to find location
            elif "where i am" in query or "where we are" in query:
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    url = "https://get,geojs.io/v1/ip/geo/"+ipAdd+".json"
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    city = geo_data["city"]
                    country = geo_data["country"]
                    speak(f"we are in {city} city of {country} country")
                except Exception as e:
                    speak("sorry, due to network issue i am not able to find the location")
                    pass
        #to take screenshot
            elif "take screenshot" in query or "take ab screenshot" in query:
                speak("please tell me the name for this screenshot file")
                name = takecommand().lower()
                speak("please hold screen for  few seconds, i am taking screenshot")
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("screenshot is saved in main folder")
        #to read pdf
            elif "read pdf" in query:
                pdf_reader()
            elif "you can sleep now" in query:
                speak("Thank you for using me, have a good day")
                sys.exit()
            # mathematical calculation




            speak("do you have any other work?")


