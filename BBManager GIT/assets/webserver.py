import http.server
import socketserver
import signal,sys
import os

def myPID():
    mypid = open("httpd_pid.txt", "w")
    pid=str(os.getpid())
    mypid.write(pid)
    mypid.close()

def stop_webserver():
    try:
        pid = open("httpd_pid.txt", "r")
        mypid=pid.read()
        pid.close()
        os.kill(int(mypid), signal.SIGINT)
        os.remove("httpd_pid.txt")
        os.remove("httpd_status.txt")
    except FileNotFoundError:
        print("Nessun server in esecuzione!")

def start_webserver(host,port): #DEFINISCO IMPOSTAZIONI WEBSERVER

    server = socketserver.ThreadingTCPServer((host, port), http.server.SimpleHTTPRequestHandler)

    # Assicura che da tastiera usando la combinazione
    # di tasti Ctrl-C termini in modo pulito tutti i thread generati
    server.daemon_threads = True
    # il Server acconsente al riutilizzo del socket anche se ancora non è stato
    # rilasciato quello precedente, andandolo a sovrascrivere
    server.allow_reuse_address = True

    # definiamo una funzione per permetterci di uscire dal processo tramite Ctrl-C
    def signal_handler(signal, frame):
        print('Exiting from http server')
        try:
            if (server):
                server.server_close()
        finally:
            sys.exit(0)

    # interrompe l’esecuzione se eseguo un sigterm da process
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    myPID()
    status = open("httpd_status.txt", "w")
    status.write(host + '\n' + str(port))
    status.close()
    # entra nel loop infinito
    try:
        while True:
            # sys.stdout.flush()
            server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

