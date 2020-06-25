#######
#@2020 Accetturi Davide - Caterina Gambetti
#This softwer is released under GPL license without any guarantee. The code is OpenSource
#BB Manager Program - This program contains all the functions to manage the server
#######

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

def start_cli(): #Function to manage the status
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
            logs=read_logs() #use local fs files to store the successifull attempt
            print(logs)
        elif choice==str(0):
            break

def bb_status():
    if os.path.exists('./logs/server_pid.log'): #read if file exists
        return "ON"
    else:
        return "OFF"

# interrompe l’esecuzione se da tastiera arriva la sequenza (CTRL + C)

def update_bbserver(newpulse,newtime):
    file=open('./config/bbsettings.config','w') #update the local variables file
    file.write("PULSE="+str(newpulse)+"\n"+"TIME="+str(newtime))
    file.close()

def start_server(pulse,time):
    def signal_handler(signal, frame): #define the sigterm signal
        try:
            print("BBServer is being closed")
        finally:
            sys.exit(0)
    status=bb_status() #update status
    if status=='OFF': #check if is already running, in case print and abort
        signal.signal(signal.SIGINT, signal_handler)
        myPID()
        listen_socket(pulse,time)
    else:
        print("BBServer is already RUNNING")

def stop_server(): #send sigterm and update log files
    try:
        pid = open("./logs/server_pid.log", "r")
        mypid=pid.read()
        pid.close()
        os.kill(int(mypid), signal.SIGINT)
        os.remove("./logs/server_pid.log")
        statusOFF() #set status off
    except FileNotFoundError: #in case no bbserver running, abort.
        print("BBServer is not running!")

def statusERR(error,p): #update bb logs with the exception
    status= open("./logs/bbserverver_status.log","w")
    status.write("ERROR: BBServer cannot start:",str(error))
    status.close()

def statusON(): ##update bb logs with on status
    status= open("./logs/bbserverver_status.log","w")
    status.write("BBServer is ON")
    status.close()

def statusOFF(): ##update bb logs with off status
    status = open("./logs/bbserverver_status.log", "w")
    status.write("BBServer is OFF")
    status.close()

def read_logs(): #read logs function and manipulate it for html views
    f = open("./logs/bb_guests_confirmed.log",'r')
    logs=f.read()
    logs=logs.replace('\n','</td></tr>')
    logs = logs.replace('A', '<tr><td>A')
    return logs

def myPID(): #function to store app PID. Necessary to kill it when is in BG
    mypid = open("./logs/server_pid.log", "w")
    pid = str(os.getpid())
    mypid.write(pid)
    mypid.close()

def add_pulse(control): #improve the pulse count in before timeout
    print("Button pressed") ##DEBUG
    global actualPULSE
    actualPULSE=actualPULSE+1

def start_evaluation(timet,pulse): #button has been pressed ONCE. Now the countdown has been started
    GPIO.remove_event_detect(18) #clean the event detection
    GPIO.add_event_detect(18, GPIO.RISING, callback=add_pulse)  # start event detection
    timeout=time.time()+int(timet) #set timeout
    while True: #start timeout
        if time.time()>=timeout:
            break
    GPIO.remove_event_detect(18) #stop thread
    global actualPULSE
    print("Number of pulses: :", actualPULSE)
    if actualPULSE!=pulse: #if real pulses matches, open the door and keep back in listen state
        open_door()

def open_door():
    log=open("./logs/bb_guests_confirmed.log",'a')
    log.write("A new guest has done the checkIN successfully on "+str(datetime.now())+"\n")
    log.close()
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
    GPIO.setup(14, GPIO.OUT)  # Setup GPIO OUT for door relay.
    GPIO.output(14, GPIO.LOW)  # Turn on Relay. (Open the door)
    time.sleep(1) #Relay Timeout
    send_email()  #Send Email
    GPIO.cleanup() #Clean the GPIO and reset them for the next cycle

def listen_socket(pulse,timet):
    try:
        statusON()
        while True:
            global actualPULSE
            actualPULSE = 0
            GPIO.setwarnings(False)  # Ignore warning for now
            GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
            GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)  # Set pin 18 to be an input pin and set initial value to be pulled low (off)
            GPIO.add_event_detect(18, GPIO.RISING)  # First push
            while True:
                if GPIO.event_detected(18):
                       break
            start_evaluation(timet,pulse)
    except Exception as e:
        statusERR(e)

def send_email(): #send email function

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
    mail = smtplib.SMTP(host=hostname, port=port) #prepare smtp connection
    mail.starttls()
    mail.login(username,password)
    msg = MIMEMultipart()  # Prepare message
    msg['From'] = "ADConsulting Domotic services "+from_address
    msg['To'] = owner_address
    msg['Subject'] = "A new guest has done correctly the check-in procedure!"
    msg.attach(MIMEText(message, 'plain'))
    mail.send_message(msg)
    del msg
    mail.quit()

