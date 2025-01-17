#######
#Copyright Accetturi Davide - Caterina Gambetti
#This software is released under GPL license without any guarantee. The code is OpenSource
#BB Manager Program - This program contains all the functions to manage the server
#######

from assets.bbmanager import *
import sys
import subprocess
import os
import time


def httpdstatus():  # AUXILIARY FUNCTION
    if os.path.exists('./logs/httpd_status.log') == True:
        return "ON"
    else:
        return "OFF"


try:
    (sys.argv[1])
    if int(sys.argv[1]) == 1:
        ##RUN WEBSERVER
        if os.name == 'nt':  # IF OS IS WINDOWS
            log = open("./logs/bg_errors_ws.log", "w")
            log.flush()
            subprocess.Popen("python" + " ./assets/runwebserver.py 0 " + str(sys.argv[2]) + " " + str(sys.argv[3]),
                             shell=True, close_fds=True)  # RUN WEBSERVER IN BG WIN
            time.sleep(5)
            if os.path.exists('./logs/httpd_pid.log') == True:  # CHECK IF WEB SERVER IS STARTING
                print("Web server is starting")  # PRINT OK
        elif os.name == 'posix':
            log = open("./logs/bg_errors_ws.log", "w")  # KEEP IN MIND WHICH IS MY PID
            log.flush
            subprocess.Popen(
                "/usr/bin/python3 " + "./assets/runwebserver.py " + str(0) + " " + str(sys.argv[2]) + " " + str(
                    sys.argv[3]), shell=True, close_fds=True)  # RUN WEBSERVER IN BG UNIX
            time.sleep(5)
            if os.path.exists('./logs/httpd_pid.log') == True:  # CHECK IF WEB SERVER IS STARTING
                print("Web server is starting")  # PRINT OK

    elif int(sys.argv[1]) == 2:
        ##RUN BBSERVER
        if os.name == 'posix':
            subprocess.Popen(
                "python3" + " ./assets/runserver.py " + str(0) + " " + str(sys.argv[2]) + " " + str(sys.argv[3]),
                shell=True, close_fds=True)  # RUN BBSERVER IN BG WIN
            time.sleep(5)
            if os.path.exists('./logs/server_pid.log') == True:  # CHECK IF BB SERVER IS STARTING
                print("BB server is starting")  # PRINT OK
        else:
            print("OS Type is not support: USE RPI!")
    elif int(sys.argv[1]) == 3:  # START CLI
        start_cli()
    elif int(sys.argv[1]) == 4:  # SHOW SERVICES STATUS
        print("BBServer is:", bb_status())
        print("HTTPDServer is:", httpdstatus())

    elif int(sys.argv[1]) == 5:
        ##DISABLE WEB SERVER
        if os.name == 'nt':  # IF OS IS WINDOWS
            log = open("./logs/bg_errors_ws.log", "w")
            subprocess.Popen("python ./assets/runwebserver.py 1 ", shell=True)  # DISABLE WEBSERVER IN BG WIN
            log.close()
            time.sleep(5)
            if os.path.exists('./logs/httpd_pid.log') == False:  # CHECK IF WEB SERVER IS STOPPED
                print("WebServer has been shut down gracefully")  # PRINT OK
        elif os.name == 'posix':
            log = open("bgerrors.txt", "w")  # TRACE ERRORS
            subprocess.Popen("/usr/bin/python3 " + "./assets/runwebserver.py 1",
                             shell=True)  # DISABLE WEBSERVER IN BG UNIX
            log.close()
            time.sleep(5)
            if os.path.exists('./logs/httpd_pid.log') == False:  # CHECK IF WEB SERVER IS STARTING
                print("WebServer has been shut down gracefully")  # PRINT OK
    elif int(sys.argv[1]) == 6:
        ##DISABLE BB SERVER
        if os.name == 'nt':  # IF OS IS WINDOWS
            log = open("./logs/bbserver_errors.log", "w")
            subprocess.Popen("python ./assets/runserver.py 1 ", shell=True)  # DISABLE WEBSERVER IN BG WIN
            log.close()
            time.sleep(5)
            if os.path.exists('./logs/server_pid.log') == False:  # CHECK IF WEB SERVER IS STOPPED
                print("BBServer has been shut down gracefully")  # PRINT OK
        elif os.name == 'posix':
            log = open("./logs/bbserver_errors.log", "w")  # TRACE ERRORS
            subprocess.Popen(
                "/usr/bin/python3 " + "./assets/runserver.py 1", shell=True)  # DISABLE WEBSERVER IN BG UNIX
            log.close()
            time.sleep(5)
            if os.path.exists('./logs/server_pid.txt') == False:  # CHECK IF WEB SERVER IS STARTING
                print("BBServer has been shut down gracefully")  # PRINT OK

except IndexError:  # IF NO ARGUMENT HAS BEEN SENT SHOW OPTIONS
    print(
        "Please, run this tool with the following argument :\n1-Start WebServer (HOST and PORT must be sent as argument)\n2-Start BBServer (PULSE and TIME must be sent as argument\n3-Start BB Cli\n4-Show Services Status\n5-Disable Web Server\n6-Disable BB Server")
