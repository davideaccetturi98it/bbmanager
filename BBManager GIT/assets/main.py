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
            subprocess.call(
                "python3" + "\\assets\\webserver.py" + str(sys.argv[2]) + str(sys.argv[3]) + "&")  # RUN WEBSERVER IN BG WIN
            time.sleep(5)
            if os.path.exists('httpd_status.txt') == True:  # CHECK IF WEB SERVER IS STARTING
                print("BB server is starting")  # PRINT OK
        elif os.name == 'posix':
            subprocess.call("/usr/bin/python3 " + "webserver.py " + str(sys.argv[2]) + " " + str(sys.argv[3]) + " &",shell=True)  # RUN WEBSERVER IN BG UNIX
            time.sleep(5)
            if os.path.exists('httpd_status.txt') == True:  # CHECK IF WEB SERVER IS STARTING
                print("BB server is starting")  # PRINT OK

    elif int(sys.argv[1]) == 1:
    ##RUN BBSERVER
            if os.name == 'nt': #IF OS IS WINDOWS
                subprocess.call("python3"+"runserver.py"+str(sys.argv[2])+str(sys.argv[3])+"&")  # RUN BBSERVER IN BG WIN
                time.sleep(5)
                if os.path.exists('status.txt') == True:  # CHECK IF BB SERVER IS STARTING
                    print("BB server is starting")  # PRINT OK
            elif os.name == 'posix':
                subprocess.call("python3"+"./assets/runserver.py"+str(sys.argv[2])+str(sys.argv[3])+"&") #RUN BBSERVER IN BG UNIX
                time.sleep(5)
                if os.path.exists('status.txt') == True: #CHECK IF BB SERVER IS STARTING
                    print("BB server is starting") #PRINT OK
            else:
                print("OS Type is not support: USE LINUX OR WINDOWS BASED PC!")
    elif int(sys.argv[1]) == 2:
        start_cli()
    elif int(sys.argv[1]) == 3:
        status()
    elif int(sys.argv[1]) == 4:
        status()

except IndexError:
    print("Please, run this tool with the following argument :\n0-Enable WebServer (HOST and PORT must be sent as argument)\n1-Start BBServer (PULSE and TIME must be sent as argument\n2-Start BB Cli\n3-Show BB Status")
