from bbmanager import start_server
from bbmanager import stop_server
import sys


#CREO IL FILE CHE INDICA I PARAMETRI RICHIESTI
if int(sys.argv[1])==0:
    if os.name == 'nt':  # IF OS IS WINDOWS
        print("BB Server is only available for RPI")
    else:
        start_server(str(sys.argv[2]),str(sys.argv[3])) #AVVIO IL SERVER CON I PARAMETRI INSERITI
elif int(sys.argv[1])==1:
    stop_server()