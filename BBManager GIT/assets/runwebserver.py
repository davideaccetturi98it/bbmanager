#######
#@2020 Accetturi Davide - Caterina Gambetti
#This softwer is released under GPL license without any guarantee. The code is OpenSource
#BB Manager Program - This program contains all the functions to manage the server
#######

from web import *
import sys
if int(sys.argv[1])==0:
    #IF START WEBSERVER
    start_webserver(str(sys.argv[2]), str(sys.argv[3]))
elif int(sys.argv[1])==1:
    #IF STOP WEBSERVER
    stop_webserver()