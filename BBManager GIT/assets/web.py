from flask import Flask,render_template,request,flash
from bbmanager import *
import subprocess
import os
import signal
import sys

def myPID():
    mypid = open("../logs/httpd_pid.log", "w")
    pid = str(os.getpid())
    mypid.write(pid)
    mypid.close()

def start_webserver(host1,port1):
    myPID() #Create PID file
    template_dir = os.path.abspath('../templates')
    static_dir=os.path.abspath('../static')
    app = Flask(__name__, template_folder=template_dir,static_folder=static_dir)
    @app.route("/")
    def main():
        return render_template('index.html')
    @app.route('/manager')
    def manager():
        return render_template('manager.html')
    @app.route('/status')
    def status():
        return render_template('status.html')
    @app.route('/api/webstatus')
    def api_webstatus():
        return web_status()
    @app.route('/api/bbstatus')
    def api_bbstatus():
        return bb_status()
    @app.route('/api/startbb',methods=["GET","POST"])
    def api_startbb():
        if request.method == "GET":
            data = bb_config()
            print(data[0])
            api_stat = subprocess.Popen("python3" + " ../main.py " + str(2) + " " + str(data[0]) + " " + str(data[1]),shell=True)  # RUN BBSERVER IN BG WIN
            return "BB Server is going to start"
        if request.method == "POST":
            timet = request.form['time']
            pulse = request.form['pulse']
            api_stat=subprocess.Popen("python3" + " ../main.py " + str(2) + " " + str(timet) + " " + str(pulse),shell=True)  # RUN BBSERVER IN BG WIN
            return "BB Server is going to restart with the new parameters"
    @app.route('/api/stopbb')
    def api_stopbb():
        api_stat = subprocess.Popen("python3" + " ../main.py " + str(6),shell=True)  # RUN BBSERVER IN BG WIN
        return api_stat
    @app.route('/api/opendoor')
    def api_door():
        api_stat = open_door()
        return "Door is opening"

    app.run(host=host1, port=port1) #RUN WEBSERVER

def stop_webserver():
    try:
        pid = open("../logs/httpd_pid.log", "r")
        mypid=pid.read()
        pid.close()
        os.kill(int(mypid), signal.SIGINT)
        os.remove("../logs/httpd_pid.log")
        os.remove("../logs/httpd_status.log")
    except FileNotFoundError:
        print("Nessun server in esecuzione!")

def web_status():
    if os.path.exists('../logs/httpd_status.log')==True:
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
    f = open('../config/bbsettings.config')
    lines = f.readlines()
    lines[0] = lines[0].rstrip("\n")
    f.close()
    return lines