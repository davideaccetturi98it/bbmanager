from bbmanager import start_server
import sys


#CREO IL FILE CHE INDICA I PARAMETRI RICHIESTI
bbserver = start_server(str(sys.argv[1]),str(sys.argv[2])) #AVVIO IL SERVER CON I PARAMETRI INSERITI
