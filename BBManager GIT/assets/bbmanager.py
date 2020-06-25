import sys,signal
import os
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import smtplib


try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
except ModuleNotFoundError:
    print("BB Server is only available on RPI based Systems")

def start_cli():
    while True:
        print("Welcome to BB Manager CLI\nPress 1 if you want disable the BB Server\nPress 2 if you want change the timeout\nPress 3 if you want see the logs\nPress 0 if you want close the CLI")
        choice = input('Choice: ')
        if choice==str(1):
            stop_server()
        elif choice==str(2):
            pulse=input('Insert the new number of pulses: ')
            time=input('Insert the new time to analyze: ')
            update_bbserver(pulse,time)
            print("The new config has been submitted. Pleas stop and start the BBServer again")
        elif choice==str(3):
            logs=read_logs()
            print(logs)
        elif choice==str(0):
            break

def bb_status():
    if os.path.exists('./logs/server_pid.log'):
        return "ON"
    else:
        return "OFF"

# interrompe l’esecuzione se da tastiera arriva la sequenza (CTRL + C)

def update_bbserver(newpulse,newtime):
    file=open('./config/bbsettings.config','w')
    file.write("PULSE="+str(newpulse)+"\n"+"TIME="+str(newtime))
    file.close()

def start_server(pulse,time):
    def signal_handler(signal, frame):
        try:
            print("BBServer is being closed")
        finally:
            sys.exit(0)
    status=bb_status()
    if status=='OFF':
        signal.signal(signal.SIGINT, signal_handler)
        myPID()
        listen_socket(pulse,time)
    else:
        print("BBServer is already RUNNING")

def stop_server(): # RIMUOVO IL FILE DI STATO
    try:
        pid = open("./logs/server_pid.log", "r")
        mypid=pid.read()
        pid.close()
        os.kill(int(mypid), signal.SIGINT)
        os.remove("./logs/server_pid.log")
        statusOFF()
    except FileNotFoundError:
        print("BBServer is not running!")

def statusERR(error,p):
    status= open("./logs/bbserverver_status.log","w")
    status.write("ERROR: BBServer cannot start:",str(error))
    status.close()

def statusON():
    status= open("./logs/bbserverver_status.log","w")
    status.write("BBServer is ON")
    status.close()

def statusOFF():
    status = open("./logs/bbserverver_status.log", "w")
    status.write("BBServer is OFF")
    status.close()

def read_logs():
    f = open("./logs/bb_guests_confirmed.log",'r')
    logs=f.read()
    logs=logs.replace('\n','</td></tr>')
    logs = logs.replace('A', '<tr><td>A')
    return logs

def myPID():
    mypid = open("./logs/server_pid.log", "w")
    pid = str(os.getpid())
    mypid.write(pid)
    mypid.close()

def add_pulse(control):
    print("Button pressed") ##DEBUG
    global actualPULSE
    actualPULSE=actualPULSE+1

def start_evaluation(timet,pulse):
    GPIO.remove_event_detect(18)
    GPIO.add_event_detect(18, GPIO.RISING, callback=add_pulse)  # Next push
    timeout=time.time()+int(timet)
    while True:
        if time.time()>=timeout:
            break
    GPIO.remove_event_detect(18)
    global actualPULSE
    print("Number of pulses: :", actualPULSE)
    if actualPULSE!=pulse:
        open_door()

def open_door():
    log=open("./logs/bb_guests_confirmed.log",'a')
    log.write("A new guest has done the checkIN successfully on "+str(datetime.now())+"\n")
    log.close()
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
    GPIO.setup(14, GPIO.OUT)  # Setup GPIO OUT for door relay.
    GPIO.output(14, GPIO.LOW)  # Turn on Relay. (Open the door)
    time.sleep(1)
    send_email()
    GPIO.cleanup()

def listen_socket(pulse,timet):
    try:
        statusON()
        while True:
            global actualPULSE
            actualPULSE = 0
            GPIO.setwarnings(False)  # Ignore warning for now
            GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
            GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
            GPIO.add_event_detect(18, GPIO.RISING)  # First push
            while True:
                if GPIO.event_detected(18):
                       break
            start_evaluation(timet,pulse)
    except Exception as e:
        statusERR(e)

def send_email():

##CONFIG PART
    hostname = "smtp.sendgrid.com"
    username = "apikey"
    password = "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"
    port = "587"
    from_address = "<domotic@adconsulting.tech>"
    owner_address ="davide@adconsulting.tech"

##MESSAGE PART
    message="A new guest has been checked-in now! "+ str(datetime.now())

##SENDING MAIL
    mail = smtplib.SMTP(host=hostname, port=port)
    mail.starttls()
    mail.login(username,password)
    msg = MIMEMultipart()  # create a message
    msg['From'] = "ADConsulting Domotic services "+from_address
    msg['To'] = owner_address
    msg['Subject'] = "A new guest has done correctly the check-in procedure!"
    msg.attach(MIMEText(message, 'plain'))
    mail.send_message(msg)
    del msg
    mail.quit()

