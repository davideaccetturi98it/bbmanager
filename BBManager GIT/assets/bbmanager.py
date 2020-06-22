import sys,signal
import os
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
import time


def start_cli():
    print("Welcome to BB Manager CLI\nPress 1 if you want disable the BB Server\nPress 2 if you want change the timeout\nPress 3 if you want see the logs\nPress 4 if you want close the CLI")
  #  while True


def status():
    if os.path.exists('status.txt')==True:
        print("BB Server is running")
    else:
        print("BB Server is not running")

def status_html():
    if status=="True":
        print("Server is running:")
    else:
        print("Server is not running")

# interrompe l’esecuzione se da tastiera arriva la sequenza (CTRL + C)

def start_server(pulse,time):
    def signal_handler(signal, frame):
        try:
            print("BB Server has been closed!")
        finally:
            sys.exit(0)
    print("BB Server is starting")
    status_start(pulse, time)
    signal.signal(signal.SIGINT, signal_handler)
    myPID()
    #RPI CODE
    GPIO_config()
    listen_socket(pulse,time)

def stop_server(): # RIMUOVO IL FILE DI STATO
    try:
        pid = open("server_pid.txt", "r")
        mypid=pid.read()
        pid.close()
        os.kill(int(mypid), signal.SIGINT)
        os.remove("server_pid.txt")
        os.remove("server_status.txt")
    except FileNotFoundError:
        print("Nessun server in esecuzione!")
def status_start(pulse,time): # CREO IL FILE DI STATO
    f = open("server_status.txt", "w")
    f.write(pulse + '\n' + time)
    f.close()

def read_logs(last):
    f = open("lastcall.txt","r")

def myPID():
    mypid = open("server_pid.txt", "w")
    pid = str(os.getpid())
    mypid.write(pid)
    mypid.close()

def start_evaluation(timet):
    timeout=time.time()+(int)timet
    while time.time()<timeout:
        GPIO.add_event_detect(22, GPIO.RISING, callback=add_pulse())  # First push
        GPIO.cleanup()  # Clean up

def GPIO_config():
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
    GPIO.setup(22, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.setup(17, GPIO.OUT)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)

def open_door():
    print("Porta aperta")

def add_pulse():
    actualPULSE=actualPULSE+1

def listen_socket(pulse,timet):
    while True:
        actualPULSE = 0
        GPIO.add_event_detect(22, GPIO.RISING, callback=start_evaluation(timet))  # First push
        if actualPULSE==pulse:
            open_door()
            break