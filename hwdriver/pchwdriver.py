# -*- coding: utf-8 -*-
from __future__ import print_function

from piodio import *
import huid
from sgnlogger import log
import sys,time

d_fname="/dev/ixpio1"

fd = PIODA_Open(d_fname)
if fd<0:
	raise Exception('IXPIO BOARD OPEN ERROR')
	huid.CUSTOMERlog("SERIVCE_HW_ERROR",d_fname)
elif 0!=PIODA_DriverInit(fd):
	raise Exception('IXPIO BOARD INIT ERROR')
	huid.CUSTOMERlog("SERIVCE_HW_ERROR",d_fname)
elif 0!=PIODA_PortDirCfs(fd, 1, DIGITAL_OUTPUT):
	raise Exception('IXPIO BOARD INIT ERROR')
	huid.CUSTOMERlog("SERIVCE_HW_ERROR",d_fname)

HIGH=1
LOW=0
BOARD='ixpio'
IN=0
OUT=1
PUD_OFF=False
PUD_UP=1
PUD_DOWN=0
RISING=1
FALING=0
BOTH=2
_ov=0

_cb22=False

def setwarnings(en):
	pass

def add_event_detect(pin,edge,callback,bouncetime=20):
	global _cb22
	if 22==pin:
		_cb22=callback

def remove_event_detect(pin):
	global _cb22
	if 22==pin:
		_cb22=False

def setmode(m):
	pass

def setup(pin, dir, pull_up_down=False):
	pass

def output(pin,state):
	#GPIO.setup(11, GPIO.OUT)	#PUMP
	#GPIO.setup(13, GPIO.OUT)	#LIGHT
	#GPIO.setup(15, GPIO.OUT)	#MAGNET
	#GPIO.setup(12, GPIO.OUT)	#DOOR UNLOCK?
	global _ov
	if 11==pin:
		p=(1<<4)
	elif 13==pin:
		p=(1<<1)
	elif 15==pin:
		p=(1<<2)
	elif 12==pin:
		p=(1<<5)
	elif 26==pin:
		p=(1<<6)
	else:
		p=-1
	if p>0:
		if state:
			_ov|=p
		else:
			_ov&=(255^p)
		PIODA_Digital_Output(fd,1,_ov)

_oss=False
_oss_ts=False
def input(pin):
	global _oss,_oss_ts
	#GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#DOOR
	#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#WATER_LOW
	#GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#MAGNET OPEN
	#GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#PULSE
	res=False
	x=WORD()	
	keyins={31:3,33:2,35:1,37:0,32:7,36:6,38:5,40:4}
	try:
		k=keyins[pin]
		PIODA_Digital_Input(fd,2,byref(x))
		res=False if 0==(x.value&(1<<k)) else True
	except:
		if 22==pin:
			k=(1<<7)
		elif 16==pin:
			k=(1<<4)
		elif 18==pin:
			k=(1<<5)
		elif 29==pin:
			k=(1<<6)
		else:
			k=0
		PIODA_Digital_Input(fd,0,byref(x))
		rs=True if (x.value&(1<<7))!=0 else False
		if rs!=_oss or not _oss_ts:
			try:
				if (not _oss_ts or (_oss_ts+0.02)<time.time()) and rs!=_oss:
					if _cb22:
						_cb22(22)
			finally:
				_oss=rs
				_oss_ts=time.time()
		if k>0:
			res=False if 0==(x.value&k) else True
	return res


