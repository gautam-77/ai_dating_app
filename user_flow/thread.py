import requests
from .models import *
import smtplib
import multiprocessing
import time
from multiprocessing.pool import Pool
from rest_framework.response import Response
import threading
from concurrent.futures import  ThreadPoolExecutor 
import random

class Thradpooltest(threading.Thread):
    def __init__(self, *args):
        self.args = args 
        threading.Thread.__init__(self)

    def run(self):
        x = random.randint(11111,99999)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("gautamsinh987@gmail.com", "mqznejfvpkkulgho")
        message = f"congratulation now you are login......... {x}" 
        s.sendmail("gautamsinh987@gmail.com", self.args, message)
        return "done"