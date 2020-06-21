import sys,signal
import http.server
import socketserver
list='127.0.0.1'
port=8081
server = socketserver.ThreadingTCPServer((list,8080), http.server.SimpleHTTPRequestHandler )
server.daemon_threads= True
server.allow_reuse_address = True

def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if( server ):
        server.server_close()
    finally:
      sys.exit(0)

#interrompe l’esecuzione se da tastiera arriva la sequenza (CTRL + C)

signal.signal(signal.SIGINT, signal_handler)

# entra nel loop infinito
try:
  while True:
    #sys.stdout.flush()
    server.serve_forever()
except KeyboardInterrupt:
  pass

server.server_close(