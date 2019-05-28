#!/usr/bin/env python

import RPi.GPIO as GPIO
import os
import re
import time
import subprocess


control="/var/www/rcam/FIFO"
dir="/dev/shm/mpir"
pid=dir + "/pid"
state=dir + "/state" 
mypid = os.getpid()

###################
#setup GPIO
###################
#
channel=22
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN)
gpiovalue = GPIO.input(channel)
print "gpio %s value = %s " % (channel,gpiovalue)

###################
# Setup control directory and files
###################
#
if not os.path.exists(dir):
	os.mkdir(dir)
pidfd = open(pid,"w")
pidfd.write(str(mypid) + "\n")
pidfd.close()

statefd = open(state,"w")
statefd.write("pause")
statefd.close()
os.chown(state,33,33)

###################
# Functions
###################

def capture(t):
	if t=="image":
		command="im 1"
	elif t=="video":
		command="ca 1 60"

	pidc = open(control,"w")
	pidc.write(command + "\n")
	pidc.close()

def alert():
        args=" -p local7.warn motion saved movie file /var/www/rcam/media\n"
        subprocess.call("/usr/bin/logger" + args, shell=True)

def checkRunning():
	#check whether we're capturing
	fo = open(state,"r") 
	str = fo.readline()
	fo.close()

	if re.match("running",str):
		return(1)

# MAIN
#
while 1:
	#need to have more than $threshold events within $interval to generate alert
	count=0
	threshold=1
	interval=60
	t=time.time()
	running=0

	while (count < threshold):
		GPIO.wait_for_edge(channel, GPIO.RISING) 
		if checkRunning():
			count += 1
			running=1
			ct=time.strftime("%x %X")
			print('Rising Edge detected '),ct
       		 	capture("image")

	if time.time() - t < interval:
		if running==1:
			print "now sending alert"
			time.sleep(1)
        		capture("video")
			alert()
			time.sleep(60)
