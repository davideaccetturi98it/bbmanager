from web import *
import sys
if int(sys.argv[1])==0:
    #IF START WEBSERVER
    start_webserver(str(sys.argv[2]), str(sys.argv[3]))
elif int(sys.argv[1])==1:
    #IF STOP WEBSERVER
    stop_webserver()