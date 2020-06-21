from bbmanager import *
import sys
import subprocess
import os
import time

#######
#SE CHIAMO CON 0 AVVIO IL WEBSERVER
#######

try:
    (sys.argv[1])
    if int(sys.argv[1]) == 0:
    ##RUN WEBSERVER
        if os.name == 'nt':  # IF OS IS WINDOWS
            log = open("bgerrors.log", "w")
            log.flush()
            subprocess.Popen("python" + " runwebserver.py 0 " + str(sys.argv[2]) + " " + str(sys.argv[3]),shell=True,stdout=log,close_fds=True)  # RUN WEBSERVER IN BG WIN
            time.sleep(5)
            if os.path.exists('httpd_status.txt') == True:  # CHECK IF WEB SERVER IS STARTING
                print("BB server is starting")  # PRINT OK
        elif os.name == 'posix':
            log = open("bgerrors.txt", "w") #KEEP IN MIND WHICH IS MY PID
            log.flush
            subprocess.Popen("/usr/bin/python3 " + "./runwebserver.py " + str(sys.argv[1]) + " " + str(sys.argv[2]) + " " + str(sys.argv[3]),shell=True,close_fds=True)  # RUN WEBSERVER IN BG UNIX
            time.sleep(5)
            if os.path.exists('httpd_status.txt') == True:  # CHECK IF WEB SERVER IS STARTING
                print("BB server is starting")  # PRINT OK

    elif int(sys.argv[1]) == 1:
    ##RUN BBSERVER
            if os.name == 'nt': #IF OS IS WINDOWS
                subprocess.call("python3"+" runserver.py"+str(sys.argv[2])+str(sys.argv[3])+"&")  # RUN BBSERVER IN BG WIN
                time.sleep(5)
                if os.path.exists('bb_status.txt') == True:  # CHECK IF BB SERVER IS STARTING
                    print("BB server is starting")  # PRINT OK
            elif os.name == 'posix':
                subprocess.call("python3"+"./assets/runserver.py"+str(sys.argv[2])+str(sys.argv[3])+"&") #RUN BBSERVER IN BG UNIX
                time.sleep(5)
                if os.path.exists('bb_status.txt') == True: #CHECK IF BB SERVER IS STARTING
                    print("BB server is starting") #PRINT OK
            else:
                print("OS Type is not support: USE LINUX OR WINDOWS BASED PC!")
    elif int(sys.argv[1]) == 2:
        start_cli()
    elif int(sys.argv[1]) == 3:
        status()
    elif int(sys.argv[1]) == 4:
        ##DISABLE WEB SERVER
        if os.name == 'nt':  # IF OS IS WINDOWS
            log = open("bgerrors.log", "w")
            subprocess.Popen("python runwebserver.py 1 ", shell=True)  # RUN WEBSERVER IN BG WIN
            log.close()
            time.sleep(5)
            if os.path.exists('httpd_status.txt') == False:  # CHECK IF WEB SERVER IS STARTING
                print("WebServer is shutting down gracefully")  # PRINT OK
        elif os.name == 'posix':
            log = open("bgerrors.txt", "w")  # TRACE ERRORS
            subprocess.Popen(
                "/usr/bin/python3 " + "./runwebserver.py 1",shell=True)  # RUN WEBSERVER IN BG UNIX
            log.close()
            time.sleep(5)
            if os.path.exists('httpd_status.txt') == True:  # CHECK IF WEB SERVER IS STARTING
                print("BB server is starting")  # PRINT OK

except IndexError:
    print("Please, run this tool with the following argument :\n0-Enable WebServer (HOST and PORT must be sent as argument)\n1-Start BBServer (PULSE and TIME must be sent as argument\n2-Start BB Cli\n3-Show BB Status")
