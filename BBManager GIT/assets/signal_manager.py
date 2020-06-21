import signal

def signal_handler(signal, frame):
    print( 'Exiting from server (Ctrl+C pressed)')
    try:
      if( server ):
        server.server_close()
    finally:
      sys.exit(0)