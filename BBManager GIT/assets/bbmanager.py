import sys,signal
import os

def start_cli():
    print("Welcome to BB Manager CLI\nPress 1 if you want disable the BB Server\nPress 2 if you want change the timeout\nPress 3 if you want see the logs\nPress 4 if you want close the CLI")

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
            status_stop()
            print("BB Server has been closed!")
        finally:
            sys.exit(0)

    print("BB Server is starting")
    status_start(pulse, time)
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        print('listen')
    #CODICE RPI

def status_stop(): # RIMUOVO IL FILE DI STATO
    os.remove("status.txt")

def status_start(pulse,time): # CREO IL FILE DI STATO
    f = open("status.txt", "w")
    f.write(pulse + '\n' + time)
    f.close()

def read_logs(last):
    f = open("lastcall.txt","r")
