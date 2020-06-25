#######
#@2020 Accetturi Davide - Caterina Gambetti
#This softwer is released under GPL license without any guarantee. The code is OpenSource
#BB Manager Program - This program contains all the functions to manage the server
#######

from flask import Flask,render_template,request,flash,redirect, url_for
from bbmanager import *
import subprocess
import os
import signal
import sys
import time

def myPID(): #function to save my pid.
    mypid = open("./logs/httpd_pid.log", "w")
    pid = str(os.getpid())
    mypid.write(pid)
    mypid.close()

def statusERR(error,p): #function to report errors
    status= open("./logs/httpd_status.log","w")
    status.write("ERROR WebServer cannot start:",str(error))
    status.close()

def statusON(): #function to set status ON
    status= open("./logs/httpd_status.log","w")
    status.write("Webserver is ON")
    status.close()

def statusOFF(): #function to set status OFF
    status = open("./logs/httpd_status.log", "w")
    status.write("Webserver is OFF")
    status.close()

def start_webserver(host1,port1): #accept in imput host and port

    try:
        ##INITIALIZATION
        myPID() #Create PID file
        template_dir = os.path.abspath('./templates') #Set Template folder (html files to be rendered)
        static_dir=os.path.abspath('./static')   #Set static folder (css,img,etc)
        app = Flask(__name__, template_folder=template_dir,static_folder=static_dir) #Create Flask app
        app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #Create Flask secret, mandatory for flash function
        ##URLS
        @app.route("/")
        def main():
            return render_template('index.html')
        @app.route('/manager')
        def manager():
            if os.name == 'nt':  # IF OS IS WINDOWS
                return "Sorry this functionality is only available on Raspberry PI based OS"
            else:
                data=bb_config()
                return render_template('manager.html',status=bb_status(),pulse=data[0],time=data[1])
        @app.route('/manager/logs')
        def logs():
            #return read_logs()
            return render_template('logs.html',displyLogs=read_logs())
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
        def api_startbb(): #analyze if function is called by a get or a push request #start function
            if request.method == "GET":
                data = bb_config()
                api_stat = subprocess.Popen("python3" + " ./main.py " + str(2) + " " + str(data[0]) + " " + str(data[1]),shell=True)  # RUN BBSERVER IN BG WIN
                time.sleep(2)
                flash('BB Server is going to start') #stamp, process is executed
                return redirect(url_for('manager'))
            if request.method == "POST":
                timet = request.form['time']
                pulse = request.form['pulse']
                update_bbserver(pulse,timet)
                api_stat = subprocess.Popen("python3" + " ./main.py " + str(6), shell=True)  # STOP BB SERVER
                time.sleep(2)
                api_stat=subprocess.Popen("python3" + " ./main.py " + str(2) + " " + str(timet) + " " + str(pulse),shell=True)  # RUN BBSERVER IN BG WIN
                time.sleep(2)
                flash('BB Server is going to restart with the new parameters')
                return redirect(url_for('manager'))
        @app.route('/api/stopbb')  #stop api
        def api_stopbb():
            api_stat = subprocess.Popen("python3" + " ./main.py " + str(6),shell=True)  # RUN BBSERVER IN BG WIN
            time.sleep(2)
            flash('BB Server is going to shut down')
            return redirect(url_for('manager'))
        @app.route('/api/opendoor') #open door api
        def api_door():
            api_stat = open_door()
            flash('Door is opening')
            return redirect(url_for('manager'))
        ##MAIN
        statusON()
        app.run(host=host1, port=port1) #RUN WEBSERVER
    except Exception as e: #store exception
        statusERR(e,p)

def stop_webserver(): #stop webserver function
    try:
        pid = open("./logs/httpd_pid.log", "r")
        mypid=pid.read()
        pid.close()
        os.kill(int(mypid), signal.SIGINT)
        os.remove("./logs/httpd_pid.log")
        statusOFF()
    except FileNotFoundError:
        print("No server in execution!")

def web_status(): #read webserver status
    if os.path.exists('./logs/httpd_status.log')==True:
        return "ON"
    else:
        return "OFF"

def bb_config(): #read bb data and use them in case we dont have set any other
    f = open('./config/bbsettings.config')
    lines = f.readlines()
    lines[0] = lines[0].rstrip("\n")
    lines[0] = lines[0].replace('PULSE=','')
    lines[1] = lines[1].rstrip("\n")
    lines[1] = lines[1].replace('TIME=','')
    f.close()
    return lines