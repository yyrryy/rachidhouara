import os
from threading import Thread
from time import sleep
import subprocess
import sys

# os.system('start /B waitress-serve 192.168.1.8 --port=80 Gro.wsgi:application')
def runserver():
    os.system('waitress-serve --host=192.168.1.8 --port=80 Gro.wsgi:application')

def lunchchrome():
    # ensure the django server is up and running
    sleep(2)
    # get ipv4 address
    os.system('start chrome http://192.168.1.8')
t1=Thread(target=runserver)

t2=Thread(target=lunchchrome)

t1.start()
sleep(2)
t2.start()