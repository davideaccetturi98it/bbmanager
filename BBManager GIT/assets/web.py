from flask import Flask,render_template,request,flash
from bbmanager import *
import subprocess
import os
import signal
import sys
import time

def myPID():
    mypid = open("./logs/httpd_pid.log", "w")
    pid = str(os.getpid())
    mypid.write(pid)
    mypid.close()

def statusERR(error,p):
    status= open("./logs/httpd_status.log","w")
    status.write("ERROR WebServer cannot start:",str(error))
    status.close()

def statusON():
    status= open("./logs/httpd_status.log","w")
    status.write("Webserver is ON")
    status.close()

def statusOFF():
    status = open("./logs/httpd_status.log", "w")
    status.write("Webserver is OFF")
    status.close()

def start_webserver(host1,port1):

    #try:
        myPID() #Create PID file
        template_dir = os.path.abspath('./templates')
        static_dir=os.path.abspath('./static')
        app = Flask(__name__, template_folder=template_dir,static_folder=static_dir)
        @app.route("/")
        def main():
            return render_template('index.html')
        @app.route('/manager')
        def manager():
            data=bb_config()
            return render_template('manager.html',status=bb_status(),pulse=data[0],time=data[1])
        @app.route('/manager/logs')
        def logs():
            return read_logs()
            #return render_template('logs.html',displyLogs=read_logs())
        @app.route('/api/webstatus')
        def api_webstatus():
            return web_status()
        @app.route('/api/bbstatus')
        def api_bbstatus():
            return bb_status()
        @app.route('/textpage')
        def textpage():
            return render_template('textpage.html')

        @app.route('/api/startbb',methods=["GET","POST"])
        def api_startbb():
            if request.method == "GET":
                data = bb_config()
                api_stat = subprocess.Popen("python3" + " ./main.py " + str(2) + " " + str(data[0]) + " " + str(data[1]),shell=True)  # RUN BBSERVER IN BG WIN
                return "BB Server is going to start"
            if request.method == "POST":
                timet = request.form['time']
                pulse = request.form['pulse']
                update_bbserver(pulse,timet)
                api_stat = subprocess.Popen("python3" + " ./main.py " + str(6), shell=True)  # STOP BB SERVER
                time.sleep(2)
                api_stat=subprocess.Popen("python3" + " ./main.py " + str(2) + " " + str(timet) + " " + str(pulse),shell=True)  # RUN BBSERVER IN BG WIN
                return "BB Server is going to restart with the new parameters"
        @app.route('/api/stopbb')
        def api_stopbb():
            api_stat = subprocess.Popen("python3" + " ./main.py " + str(6),shell=True)  # RUN BBSERVER IN BG WIN
            return "BB Server is going to shut down. Thanks for using our product"
        @app.route('/api/opendoor')
        def api_door():
            api_stat = open_door()
            return "Door is opening"
        statusON()
        app.run(host=host1, port=port1) #RUN WEBSERVER
   # except Exception as e:
   #     statusERR(e,p)

def stop_webserver():
    try:
        pid = open("./logs/httpd_pid.log", "r")
        mypid=pid.read()
        pid.close()
        os.kill(int(mypid), signal.SIGINT)
        os.remove("./logs/httpd_pid.log")
        statusOFF()
    except FileNotFoundError:
        print("Nessun server in esecuzione!")

def web_status():
    if os.path.exists('./logs/httpd_status.log')==True:
        return "ON"
    else:
        return "OFF"

def bb_config():
    #with open('../config/bbsettings.config') as f:
    #    data = {}
    #    for line in f:
    #        key, value = line.strip().split('=')
    #        data[key] = value
    #return data
    f = open('./config/bbsettings.config')
    lines = f.readlines()
    lines[0] = lines[0].rstrip("\n")
    lines[0] = lines[0].replace('PULSE=','')
    lines[1] = lines[1].rstrip("\n")
    lines[1] = lines[1].replace('TIME=','')
    f.close()
    return lines