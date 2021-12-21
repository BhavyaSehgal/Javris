import operator
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import PyPDF2
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
from JavrisUi import Ui_MainWindow
import pyttsx3 #provide engine -- convert text to voice
import speech_recognition as sr #to take command for user
import datetime
import os
import cv2
from requests import get
import requests
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import pyjokes
import pyautogui
import pywikihow



engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)#voices[0] = male or female voice of javaris

#fnction to convert text to audio
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

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

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()
    def run(self):
        #self.TaskExceution()
        speak("Please say wakeup to continue")
        while True:
            self.query = self.takecommand()
            if "wake up" in self.query or "are you there" in self.query or "hello" in self.query:
                self.TaskExecution()

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening ....")
            r.pause_threshold = 1  # if user stops while speaking javaris doenot shutdown
            audio = r.listen(source, timeout=1000, phrase_time_limit=5)
        try:
            print("Recognized")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said : {self.query}")

        except Exception as e:
            speak("Say that again please...")
            return "none"
        query = query().lower()

        return query


    def TaskExecution(self):
        wish()
        while True:
            if 1:
                self.query = self.takecommand().lower()

                #logic building for tasks

                if "open notepad" in self.query:
                    npath = "C:\\WINDOWS\\system32\\notepad.exe"
                    os.startfile(npath)
                elif "open command prompt" in self.query:
                    os.system('start cmd')
                elif "open camera" in self.query:
                    cap = cv2.VideoCapture(0)
                    while True:
                        ret, img = cap.read()
                        cv2.imshow('webcam',img)
                        k=cv2.waitKey(50)
                        if k == 27:
                            break
                    cap.release()
                    cv2.destroyAllWindows()
                    #press escape to shutdown camera
                elif "play music" in self.query:
                    music_dir = "D:\\bhavya\\Music"
                    songs = os.listdir(music_dir)
                    os.startfile(os.path.join(music_dir,songs[0]))
                elif "ip address" in self.query:
                    ip = get('https://api.ipify.org').text
                    speak(f"your IP address is {ip}")
                elif "wikipedia" in self.query:
                    speak("searching wikipedia...")
                    self.query = self.query.replace("wikipedia","")
                    result = wikipedia.summary(self.query, sentences = 2)
                    speak("According to wikipedia")
                    speak(result)
                    #print(result)
                elif "open youtube" in self.query:
                    webbrowser.open("www.youtube.com")
                elif "open stack overflow" in self.query:
                    webbrowser.open("www.stackoverflow.com")
                elif "open instagram" in self.query:
                    webbrowser.open("www.instagram.com")
                elif "open google" in self.query:
                    speak("What should I search on google")
                    cm = self.takecommand().lower()
                    webbrowser.open(f"{cm}")
                elif "send message" in self.query:
                    kit.sendwhatmsg('+916283447051',"this is testing protocol",2,25)
                elif "play song on youtube" in self.query:
                    kit.playonyt("Kasoor")
                elif "send email" in self.query:
                    speak("what should I  send")
                    content = self.takecommand().lower()
                    if "send a file" in content:
                        email = "bhavyasehgal4241@gmail.com"
                        password = "Gndu#4241"
                        send_to_mail = "bhavyasehgal4241@gmail.com"
                        speak("what should be subject od mail")
                        self.query1 = self.takecommand().lower()
                        subject = self.query1
                        speak("what is message of mail")
                        self.query2 = self.takecommand().lower()
                        message = self.query2
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
                elif "close notepad" in self.query:
                    speak("okay, closing notepad")
                    os.system("taskkill /f /im notepad.exe")
                #to set alarm
                elif "alarm" in self.query:
                    speak("please tell me the time to set alarm. for exqample, set alarm to 5:30 AM")
                    tt = self.takecommand()
                    tt = tt.replace("set alarm to ", "")
                    tt= tt.replace(".","")
                    tt=tt.upper()
                    import MyAlarm
                    MyAlarm.alarm(tt)
                #to tell joke
                elif "tell a joke" in self.query:
                    joke = pyjokes.get_joke()
                    speak(joke)
                elif "shut down the system" in self.query:
                    os.system("shutdown /s /t 5")
                elif "restart the system" in self.query:
                    os.system("shutdown /r /t 5")
                elif "sleep the system" in self.query:
                    os.system("rundll32.exe powrprof.dll, SetSuspendtate 0,1,0")
                elif "tell me news" in self.query:
                    speak("please wait,fetching the latest news")
                    news()
                elif "switch the window" in self.query:
                    pyautogui.keyDown("alt")
                    pyautogui.press("tab")
                    time.sleep(1)
                    pyautogui.keyUp("alt")
                #to find location
                elif "where i am" in self.query or "where we are" in self.query:
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
                elif "take screenshot" in self.query or "take ab screenshot" in self.query:
                    speak("please tell me the name for this screenshot file")
                    name = self.takecommand().lower()
                    speak("please hold screen for  few seconds, i am taking screenshot")
                    time.sleep(3)
                    img = pyautogui.screenshot()
                    img.save(f"{name}.png")
                    speak("screenshot is saved in main folder")
            #to read pdf
                elif "read pdf" in self.query:
                    pdf_reader()
                elif "you can sleep now" in self.query:
                    speak("okay i am going to sleep, you can call me anytime")
                    break
                # mathematical calculation
                elif "do some calculation" in self.query or "can you calculate" in self.query:
                    r = sr.Recognizer()
                    with sr.Microphone() as source:
                        speak("What do you want to calculate, like 3 plus 3") # if user stops while speaking javaris doenot shutdown
                        print("listening ....")
                        r.adjust_for_ambient_noise(source)
                        audio = r.listen(source, timeout=1000, phrase_time_limit=5)
                        my_string = r.recognize_google(audio)
                        print(my_string)
                        def get_operator_fn(op):
                            return{
                                '+' : operator.add,
                                '-' : operator.sub,
                                '*' : operator.mul,
                                'divided' : operator.__truediv__,
                            }[op]
                        def eval_binary_expr(op1,oper,op2):
                            op1,op2 = int(op1),int(op2)
                            return get_operator_fn(oper)(op1,op2)
                        speak("your result is: ")
                        speak(eval_binary_expr(*(my_string.split())))
                elif "temperature" in self.query:
                    search = "temperature in Delhi"
                    url = f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp =data.find("div",class_="BNeawe").text
                    speak(f"current{search} is {temp}")
                elif "activate how to do mode" in self.query:
                    speak("How to do mode is activated")
                    while True:
                        speak("please tell me what to know")
                        how = self.takecommand()
                        try:
                            if "exit" in how or "close" in how:
                                speak("Okay sir, how to mode is closed")
                                break
                            else:
                                max_results = 1
                                how_to = pywikihow.search_wikihow(how, max_results)
                                assert len(how_to)==1
                                how_to[0].print()
                                speak(how_to[0].summary)
                        except Exception as e:
                            speak("Sorry sir, I am not able to find this")
                elif "how much power left" in self.query or "how much power we have" in self.query or "battery" in self.query:
                    import psutil
                    battery = psutil.sensors_battery()
                    percentage = battery.percent
                    speak(f"Our system have {percentage} percent battery")
                    if percentage>=75:
                        speak("We have enough power to continue our work")
                    elif percentage>=40 and percentage<=75:
                        speak("We should connect our system to charger")
                    elif percentage<=15 and percentage<=30:
                        speak("We don't have enpugh power to work, please connect to charger")
                    elif percentage<=1:
                        speak("We have very low power, the system will shutdown very soon")
                elif "internet speed" in self.query:
                    import speedtest
                    st = speedtest.Speedtest()
                    dl = st.download()
                    up = st.upload()
                    speak(f"we have {dl} bit per second downloading speed and {up} bit per second uploading speed")
                elif "send message" in self.query:
                    speak("What should I send")
                    msz = self.takecommand()
                    from twilio.rest import Client
                    account_sid = 'AC0f27b3ee78e883fd0fa3b8e40c62d354'
                    auth_token = '1c7fcab3fce5dbdc3f8d0b5f38307425'
                    client = Client(account_sid,auth_token)
                    message = client.messages \
                        .create(
                        body='This is the ship that made the Kessel Run in fourteen parsecs?',
                        from_='+14054495026',
                        to='7589170339'
                    )
                    print(message.sid)
                elif "call" in self.query or "phone" in self.query:
                    from twilio.rest import Client
                    account_sid = 'AC0f27b3ee78e883fd0fa3b8e40c62d354'
                    auth_token = '1c7fcab3fce5dbdc3f8d0b5f38307425'
                    client = Client(account_sid, auth_token)
                    call = client.calls \
                        .create(
                        twiml='<Response><Say>This is second testing message from Javris side...</Say></Response>',
                        from_='+14054495026',
                        to='7589170339'
                    )
                    print(call.sid)
                elif "Volume up" in self.query:
                    pyautogui.press("Volumeup")
                elif "Volume down" in self.query:
                    pyautogui.press("volumedown")
                elif "volume mute" in self.query:
                    pyautogui.press("volumemute")

                speak("do you have any other work?")

    if __name__=="__main__":
        while True:
            permission = takecommand()
            if "wake up" in permission:
                TaskExecution()
            elif "goodbye" in permission:
                speak("Thanks for using me, have a good day")
                sys.exit()

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
    def startTask(self):
        self.ui.movie = QtGui.QMovie("7LP8.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("7LP8.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()
    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString("hh:mm:ss")
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())



