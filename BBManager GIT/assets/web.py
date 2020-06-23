from flask import Flask,render_template,request
from bbmanager import bb_status
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
        if request.method == "POST":
            timet = request.form['time']
            pulse = request.form['pulse']
        api_stat=subprocess.Popen("python3" + " main.py " + str(2) + " " + str(timet) + " " + str(pulse),shell=True)  # RUN BBSERVER IN BG WIN
        return "Command Executed!"
    @app.route('/api/stopbb')
    def api_stopbb():
        api_stat = subprocess.Popen("python3" + " main.py " + str(6),shell=True)  # RUN BBSERVER IN BG WIN
        return api_stat

    app.run(host=host1, port=port1)

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