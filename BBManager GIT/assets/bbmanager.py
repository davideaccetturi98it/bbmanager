import sys,signal
import os
import time

try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
except ModuleNotFoundError:
    print("BB Server is only available on RPI based Systems")

def start_cli():
    print("Welcome to BB Manager CLI\nPress 1 if you want disable the BB Server\nPress 2 if you want change the timeout\nPress 3 if you want see the logs\nPress 4 if you want close the CLI")
  #  while True


def bb_status():
    if os.path.exists('./logs/bbserver_status.log'):
        return "ON"
    else:
        return "OFF"

# interrompe l’esecuzione se da tastiera arriva la sequenza (CTRL + C)

def start_server(pulse,time):
    def signal_handler(signal, frame):
        try:
            print("BB Server has been closed!")
        finally:
            sys.exit(0)
    status=bb_status()
    if status=='OFF':
        #status_start(pulse, time)
        signal.signal(signal.SIGINT, signal_handler)
        myPID()
        #RPI CODE
        listen_socket(pulse,time)
    else:
        return "Server is already RUNNING"

def stop_server(): # RIMUOVO IL FILE DI STATO
    try:
        pid = open("./logs/server_pid.log", "r")
        mypid=pid.read()
        pid.close()
        os.kill(int(mypid), signal.SIGINT)
        os.remove("./logs/server_pid.log")
        os.remove("./logs/bbserver_status.log")
    except FileNotFoundError:
        print("Nessun server in esecuzione!")

def status_start(pulse,time): # CREO IL FILE DI STATO
    f = open("./logs/bbserverver_status.log", "w")
    f.write(pulse + '\n' + time)
    f.close()

def read_logs(last):
    f = open("lastcall.txt","r")

def myPID():
    mypid = open("./logs/server_pid.log", "w")
    pid = str(os.getpid())
    mypid.write(pid)
    mypid.close()

def add_pulse(control):
    print("Pulsante Premuto") ##DEBUG
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
    print("Numero pulsazioni:", actualPULSE)
    if actualPULSE!=pulse:
        open_door()

def open_door():
    print("Apro porta")
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
    GPIO.setup(14, GPIO.OUT)  # Setup GPIO OUT for door relais.
    GPIO.output(14, GPIO.LOW)  # Turn on Relais. (Open the door)
    time.sleep(1)
    GPIO.cleanup()

def listen_socket(pulse,timet):

    try:
        file=open("./logs/bbserver_status.log","w")
        file.write("ON")
        file.close()
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
        print("An error occured:",e)