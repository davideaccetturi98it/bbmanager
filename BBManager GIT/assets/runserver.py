#######
#@2020 Accetturi Davide - Caterina Gambetti
#This softwer is released under GPL license. The code is OpenSource
#Main Program - It calls other functions from assets.
#######

from bbmanager import start_server
from bbmanager import stop_server
import sys
import os

#CHECK IF OS IS WINDOWS. IN CASE ABORT
if int(sys.argv[1])==0:
    if os.name == 'nt':  # IF OS IS WINDOWS
        print("Sorry, BB Server is only available for RPi.")
    else:
        start_server(str(sys.argv[2]),str(sys.argv[3])) #RUN SERVER WITH THE RIGHT VALUE
elif int(sys.argv[1])==1: #STOP SERVER
    stop_server()