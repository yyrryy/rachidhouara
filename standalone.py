import os
from threading import Thread
from time import sleep
import socket
import sys

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = 'localhost'
    finally:
        s.close()
    return ip
ip = get_local_ip()
def runserver():
    os.system(f'python manage.py runserver {ip}:80')

def lunchchrome():
    # ensure the django server is up and running
    sleep(2)
    # get ipv4 address
    os.system(f'start chrome http://{ip}:80')
t1=Thread(target=runserver)

t2=Thread(target=lunchchrome)

t1.start()
sleep(2)
t2.start()

#pause

pause = input("Press Enter to stop the server...")