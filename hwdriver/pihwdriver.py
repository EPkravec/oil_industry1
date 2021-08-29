# -*- coding: utf-8 -*-
# encoding: utf-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logging
import threading
from traceback import format_exc
import time
#import kiosk
from sgnlogger import log

#import keyboard
from twisted.internet import reactor, protocol, endpoints
from datetime import datetime
from twisted.internet.task import LoopingCall

import simplejson as json

enable_avr_flash=False

try: 
	import RPi.GPIO as GPIO
	hasRPi=True
except:
	log.error("RPi.GRIO module not found!")	
	hasRPi=False
	try:
		import pchwdriver as GPIO
	except:
		log.error("PIODIO module not found!")	

_kip=False
gp=None

pulse_start_value=8
cur_pulse_start_value=False
nlv_pzc=0

#odt=time.time()
#def bottle_door_irq(chn):
#	gp=getGPIO()
#	st=GPIO.input(chn)
#	if not st:
#		gp.bottle_door_timeout=time.time()
#	else:
#		gp.bottle_door_timeout=False
_has_irq_error=False
def pulse_irq(chn):
	try:
		global gp,cur_pulse_start_value
		#log.info('PULSE IRQ %s'%gp.pulse_cnt)	
		if gp.pulse_cnt:
			ts=time.time()#-gp.pump_timeout
			#if gp.pulse_passed>5 and ts<(gp.pulse_prev*0.6):
			#	gp.pulse_prev=(gp.pulse_prev+ts)/2
			#	gp.getLogger().error('[GPIO - PULSE] ПОМЕХА!!!!!!: %.01fмс осталось: %d'%(ts*1000,gp.pulse_cnt))
			#	return	#TOO EARLY
			#if 0==gp.pulses:
			if cur_pulse_start_value:
				cur_pulse_start_value=False
				gp.pulses+=pulse_start_value
				gp.pulse_cnt-=pulse_start_value
				if gp.pulse_cnt<1:
					gp.pulse_cnt=1

			gp.pulses+=1
			gp.pulse_cnt-=1
			if gp.rst_pulse_changed:
				gp.rst_pulse_changed=False
				gp.pulse_changed=0
			#gp.send_mutex.acquire()
			gp.pulse_changed+=1
			#gp.send_mutex.release()
			#gp.pulse_prev=ts
			#gp.pump_timeout=time.time()
			gp.pulse_changed+=1

			if gp.pause_req:
				x=gp.pause_req-gp.pulses
				log.warn('ПАУЗА БУДЕТ ЧЕРЕЗ %s'%x)
				if gp.pump and not gp.pump_paused and x<=0:
					log.warn('ОТЛОЖЕННАЯ ПАУЗА')
					gp.pump_paused=True
					gp.update_outputs()

			elif gp.pulses==3 and gp.pulse_cnt>40:
				if gp.pump and not gp.pump_paused:
					if not enable_avr_flash:
						GPIO_output(7, GPIO.HIGH)
					gp.pump_aux=True
			elif gp.pulse_cnt==7:
				if not enable_avr_flash:
					GPIO_output(7, GPIO.LOW)
				gp.pump_aux=False

			if gp.pump_aux and gp.pulse_cnt>10 and gp.pulses>10:
				ffr=ts-gp.pulse_prev
				if not gp.avgr:
					gp.avgr=ffr
				else:
					gp.avgr=(ffr*0.1)+(gp.avgr*0.9)

			gp.pulse_prev=ts
			gp.pump_timeout=time.time()

			#log.info('[GPIO - PULSE] импульс: %.01fмс осталось: %d'%(ts*1000,gp.pulse_cnt))
		else:
			if gp.pump:
				gp._pulse_more=0;
				gp.pump=False
				gp.pump_done=True
				gp.update_outputs()
			elif gp.pump_timeout:
				if (time.time()-gp.pump_timeout)<gp.cfg['water']['valve']['closing_time']:
					gp._pulse_more+=1
					#log.info('[GPIO - PULSE] доп импульс! лишних: %d время: %d с'%(gp._pulse_more,(time.time()-gp.pump_timeout)))

			#GPIO_output(17, GPIO.HIGH if not self.pump else GPIO.LOW)
	except:
		global _has_irq_error
		if not _has_irq_error:
			_has_irq_error=True
			log.failure('ОШИБКА В ПРЕРЫВАНИИ')


_pins=dict()
def GPIO_output(pin,value):
	global _pins
	if not (pin in _pins) or _pins[pin]!=value:
		_pins[pin]=value
		GPIO.output(pin,value)

class PiGPIO:
#INPUTS:
#define BUY_L19 RPI_BPLUS_GPIO_J8_31    //RPI_V2_GPIO_P1_6
#define BUY_L12 RPI_BPLUS_GPIO_J8_33    //RPI_V2_GPIO_P1_13
#define BUY_L5 RPI_BPLUS_GPIO_J8_35     //RPI_V2_GPIO_P1_19
#define BUY_START RPI_BPLUS_GPIO_J8_37  //RPI_V2_GPIO_P1_26
#define BUY_BOTTLE RPI_BPLUS_GPIO_J8_32   //RPI_V2_GPIO_P1_12
#define BUY_CARD RPI_BPLUS_GPIO_J8_36   //RPI_V2_GPIO_P1_16
#define UPDATE_CARD RPI_BPLUS_GPIO_J8_38 //RPI_V2_GPIO_P1_20
#define BUY_PAYOUT RPI_BPLUS_GPIO_J8_40 //RPI_V2_GPIO_P1_21
#define DOOR RPI_BPLUS_GPIO_J8_16   //RPI_V2_GPIO_P5_06
#define LSSL RPI_BPLUS_GPIO_J8_18   //RPI_V2_GPIO_P1_24
#define MAGNET_OPEN RPI_BPLUS_GPIO_J8_29 // 5
#define IMPULSE RPI_BPLUS_GPIO_J8_22 // 5

#OUTPUTS:
#define MOTOR RPI_BPLUS_GPIO_J8_11
#define LED RPI_BPLUS_GPIO_J8_13
#define MAGNET RPI_BPLUS_GPIO_J8_15
#define DOOR_OPEN RPI_BPLUS_GPIO_J8_12   //RPI_V2_GPIO_P1_18
#PIN 26 "GPIO7/SPI_CE1" через VT16 управляет насосом отдельно от клапана

	def addeventdetect(self):
		self.detecting=True
		#GPIO.add_event_detect(22, GPIO.BOTH, callback=pulse_irq, bouncetime=1)

	def removeeventdetect(self):
		self.detecting=False
		#GPIO.remove_event_detect(22)

	def __init__(self,factory,disabled=False):
		global gp
		gp=self
		self._i_level=False
		self.detecting=False
		self._wash=self.wash=False
		self.emulation=False
		self.factory=factory
		self.send_mutex=threading.RLock()
		self.pulse_more=8
		self._pulse_more=0
		self.pulse_cnt=0
		self.pulse_passed=0
		self.pump_timeout=0
		self.pump_done=False
		self.pump_paused=False
		self._bottle_price=0
		self.pulse_changed=0
		self.rst_pulse_changed=False
		self.was_paused=False
		self.bottle_door_timeout=False
		self.bottle_sold_time=False
		self.disabled=disabled
		self.door_unlock_time=False
		self.keyins=[6,13,19,26,12,16,20,21]
		self.ks=[1,1,1,1,1,1,1,1]
		self.rpt=False
		self.minpulses=0
		self.pause_req=False
		self.isopen=False
		self.freeze_pulses=False
		self.avgr=False
		self.fa=0
		self.ra=0
		self._bse=False
		self._bsto=False
		self._bxto=False
		self.reddis=True
		self.pulse_coef=1.0
		self.pulse_add_value=0
		self.has_modbus=False
		self.pause_ts=False
		self.nokeydown=False
		log.warn('CREATING GPIO OBJECT')
		if not disabled:
			log.warn('INIT INPUTS')
			#GPIO.setmode(GPIO.BOARD)
			GPIO.setmode(GPIO.BCM)
			for k in self.keyins:
				GPIO.setup(k, GPIO.IN, pull_up_down=GPIO.PUD_UP)
				#GPIO.setup(k, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
			self.getKeyState()
			GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#DOOR
			GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#WATER_LOW
			GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#MAGNET OPEN
			GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#PULSE

			log.warn('INIT IRQ')
			self.addeventdetect() #GPIO.add_event_detect(25, GPIO.BOTH, callback=pulse_irq, bouncetime=10)

			#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_OFF)	#DOOR
			#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_OFF)	#WATER_LOW
			#GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_OFF)	#MAGNET OPEN
			#GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_OFF)	#PULSE

			# add rising edge detection on a channel, ignoring further edges for 80ms for switch bounce handling
			#GPIO.add_event_detect(25, GPIO.RISING, callback=pulse_irq)
			#GPIO.add_event_detect(25, GPIO.BOTH, callback=pulse_irq, bouncetime=50)
			#GPIO.add_event_detect(5, GPIO.BOTH, callback=bottle_door_irq, bouncetime=100)

			self.pulses=0
			self.pump=False
			self.light=False
			self.mag_bottle=False
			self.door_unlock=False
			self.pump_aux=False
			self.oldst=None
			log.warn('INIT OUTPUTS')
			GPIO.setwarnings(False)
			GPIO.setup(17, GPIO.OUT)	#PUMP
			GPIO.setup(27, GPIO.OUT)	#LIGHT
			GPIO.setup(22, GPIO.OUT)	#MAGNET
			GPIO.setup(18, GPIO.OUT)	#DOOR UNLOCK?

			if not enable_avr_flash:
				GPIO.setup(7, GPIO.OUT)	#PUMP AUX
				#GPIO_output(26, GPIO.LOW)

			GPIO.setwarnings(True)
			log.warn('Updating Outputs')
			self.update_outputs()

			log.warn('INIT POLL')

			lc = LoopingCall(self.poll)
			lc.start(0.01)

			log.warn('INIT DONE')

			#keyboard.press_and_release('Shift')

					#self.pollevent=threading.Condition()
		#self.waterevent=threading.Condition()

		import yaml

		try:
			config='/etc/kiosk/options.yaml'
			f = open(config,"r")
			cfg=yaml.load(f)
			f.close();
			a=cfg['water']['flowmeter']
		except:
			log.failure("Cannot read %s"%config)
			cfg=dict(water=dict(
				flowmeter=dict(resolution=0.012),
				valve=dict(pulses=0,closing_time=1.5),
				pause_add=5,
				correction=dict(enabled=False,permissions=dict(enable_pulses_more=True,enable_fringe=False)),
				fringe_frequency=10.0))
			f = open(config,"w")
			f.write(yaml.dump(cfg))
			f.close();
		self.cfg=cfg


	def recalc_pulses(self,pls):
		p=int(round(self.pulse_coef*pls))
		"""
		if p>0:
			p-=self.pulse_add_value
			if p<1:
				p=1
		"""
		return p


	def update_outputs(self):
		if not self.disabled:
			GPIO_output(17, GPIO.LOW if not (self.pump and not self.pump_paused) else GPIO.HIGH)
			GPIO_output(27, GPIO.LOW if not self.light else GPIO.HIGH)
			GPIO_output(22, GPIO.LOW if not self.mag_bottle else GPIO.HIGH)
			GPIO_output(18, GPIO.LOW if not self.door_unlock else GPIO.HIGH)
			if not self.pump or self.pump_paused:
				if not enable_avr_flash:
					GPIO_output(7, GPIO.LOW)
				self.pump_aux=False
				self.wash=False
			elif gp.pulses>10 and gp.pulse_cnt>40:
				if not enable_avr_flash:
					GPIO_output(7, GPIO.HIGH)
				self.pump_aux=True
			isopen=(self.pump and not self.pump_paused)
			if isopen!=self.isopen:				
				self.isopen=isopen
				if self.avgr and self.avgr>0:
					self.fa=1.0/self.avgr
					self.ra=0.024*self.fa*60.0
				else:
					self.ra=0
					self.fa=0
				log.warn('СМЕНА СТАТУСА ПРОТОКА ВОДЫ: %s СРЕДНИЙ РАСХОД: %.03fл/мин, СРЕДНЯЯ ЧАСТОТА: %.02fHz'%('Течет' if isopen else 'Перекрыт',self.ra,self.fa))
				if not isopen:
					self.freeze_pulses=self.pulses


	def getState(self):
		xstate = dict(
			pump=self.pump,
			pump_paused=self.pump_paused,
			pump_aux=self.pump_aux,
			light=self.light,
			bottle_locked=not self.mag_bottle,
			door_locked=not self.door_unlock,
			bottle_open=not GPIO.input(5),
			water_low=not GPIO.input(24),
			door_open=not GPIO.input(23),
			emulation=self.emulation,
			flowmeter_state=GPIO.input(25) if not (self.pump and not self.pump_paused) else False,
			flow=self.ra,
			flowmeter_frequency=self.fa,
			modbus=self.has_modbus,
			)
		if self.emulation:
			if (self.mag_bottle and (time.time()-self.bottle_sold_time)>5) or (self.bottle_door_timeout and (time.time()-self.bottle_door_timeout)<10):
				xstate['bottle_open']=True
				if not self.bottle_door_timeout:
					self.bottle_door_timeout=time.time()

		return xstate

	def stateSend(self):
		self.factory.send_to_all((u'STATE %s'%json.dumps(self.getState())).encode())

	def terminate(self):
		opp=self.pump
		self.removeeventdetect()#GPIO.remove_event_detect(25)
		self.pump=False
		self.pump_paused=False
		self.light=False
		self.mag_bottle=False
		self.door_unlock=False
		self.update_outputs()
		if opp:
			self.setPulseCounter(False)			

	def getKeyState(self):
		if self.disabled:
			ret=[1,1,1,1,1,1,1,1]
		else:
			ret=[]
			db=''
			for k in self.keyins:
				ins=GPIO.input(k)
				ret.append(ins)
				db=db+('%x '%ins)
			#self.getLogger().debug('[GPIO] keys: '+db)
			self.ks=ret
		return ret

	def poll(self):
		try:
			pe=False
			oks=self.ks
			self.getKeyState()
			for i in range(0,len(self.ks)):
				try:
					if 0==self.ks[i] and 1==oks[i]:
						self.notifyKeyDown(i+1)
						pe=True
					elif 1==self.ks[i] and 0==oks[i]:
						self.notifyKeyUp(i+1)
						pe=True
				except Exception, e:
					log.failure('KEYBOARD EMULATION ERROR')

			if self.rpt:
				if (self.rpt[1]+self.rpt[0])<time.time():
					if self.rpt[0]>0.19:
						self.rpt[0]-=0.1
					self.rpt[1]=time.time()
					try:
						self.factory.send_to_all((u'KEY_REPEAT %d'%self.rpt[2]).encode())
					except:
						log.failure('KEYBOARD REPEAT ERROR')

			if self.emulation and self.pump and not self.pump_paused:
				pulse_irq(5)
			else:
				_lvl=GPIO.input(25)
				if _lvl!=self._i_level:
					self._i_level=_lvl
					if self.detecting:
						pulse_irq(25)


			if self.door_unlock and (not self.door_unlock_time or (self.door_unlock_time+1.5)<time.time()):
				self.door_unlock=False
				self.door_unlock_time=False

			self.update_outputs()
			state=self.getState()

			if self.oldst!=state:
				self.oldst=state
				self.stateSend()

			if state['bottle_open']:
				if not self.bottle_door_timeout and self.mag_bottle:
					if not self._bxto:
						self._bxto=time.time()
					elif (time.time()-self._bxto)>0.5:
						self.bottle_door_timeout=time.time()
						log.info('[GPIO] Дверца бутылей открыта, включаем магнит снова!')
				if self.bottle_sold_time:
					#if not self._bxto or (time.time()-self._bxto)>0.3:
					self.bottle_sold_time=False
					self.notifyBottleSold()
				else:
					if not self._bsto:
						self._bsto=time.time()
					elif (self._bsto+5)<time.time():
						if not self._bse:
							self._bse=time.time()
							import huid
							huid.CUSTOMERlog('BOTTLE_STOLEN','')					
			else:
				self._bxto=False
				self._bsto=False
				if self._bse and (self._bse+3600)<time.time():
					self._bse=False
				if self.bottle_sold_time:
					self.bottle_door_timeout=False

			if self.mag_bottle:							
				if self.bottle_door_timeout and (time.time()-self.bottle_door_timeout)>0.1:
					self.mag_bottle=False
					if not self.emulation:
						self.bottle_door_timeout=False
					log.info('Магнит отключен')

				if self.bottle_sold_time and self.mag_bottle and (time.time()-self.bottle_sold_time)>30:
					self.mag_bottle=False
					self.bottle_sold_time=False
					self.notifyBottleNotSold()

			tot=False
			self.send_mutex.acquire()
			try:
				if self.pulse_changed>(10 if self.fa<10 else self.fa) or self.pump_paused and (self.pulse_changed>0 or self.pause_req):
					if self.pump:
						if self.pump_paused:
							self.pause_req=False
						if self.pump_paused:
							log.warn('PAUSE SENT 0 pulses: %s pulses_changed: %s'%(self.pulses,self.pulse_changed))
						if not self.pump_paused or not self.pause_ts or (self.pause_ts+2)<time.time():
							self.factory.send_to_all((u'PUMP %s %d'%('ENPAUSED' if self.pump_paused else 'ON',self.recalc_pulses(self.pulses if not self.freeze_pulses else self.freeze_pulses))).encode())
						else:							
							self.factory.send_to_all((u'PUMP PAUSED %d'%self.recalc_pulses(self.pulses if not self.freeze_pulses else self.freeze_pulses)).encode())
						self.pulse_changed=0
						self.rst_pulse_changed=True
			finally:
				self.send_mutex.release()
			#if tot:
			#	kiosk.kiosk_logic.getKIOSK().salePollSold(tot)

			if self.pump_done:
				self.pump_done=False
				self.notifyPumpDone()
			elif self.pump and self.pump_timeout and (time.time()-self.pump_timeout)>(3 if not self.pause_ts or (self.pause_ts+2)<time.time() else 1):
				if self.pump_paused:
					self.pump_timeout=time.time()
					if not self.pause_ts or (self.pause_ts+2)<time.time():
						log.warn('PAUSE SENT 1')
						self.factory.send_to_all((u'PUMP ENPAUSED %d'%self.recalc_pulses(self.pulses if not self.freeze_pulses else self.freeze_pulses)).encode())
					else:
						self.factory.send_to_all((u'PUMP PAUSED %d'%self.recalc_pulses(self.pulses if not self.freeze_pulses else self.freeze_pulses)).encode())
				else:
					if (time.time()-self.pump_timeout)>150 and self.reddis:
						log.error('RE-ENABLING IRQ')
						self.reddis=False
						self.removeeventdetect()#GPIO.remove_event_detect(25)
						self.addeventdetect() #GPIO.add_event_detect(25, GPIO.BOTH, callback=pulse_irq, bouncetime=10)
					if not self.wash or (time.time()-self.pump_timeout)>300:						
						log.error('WATER TIMEOUT')
						self.pause_req=False
						self.pump=False
						self.pump_paused=False
						self.pulse_cnt=0
						self.pump_timeout=False
						self.notifyPumpTimeout()
			elif self.pump_timeout and (time.time()-self.pump_timeout)>5:
				self.pulse_more=(self.pulse_more+self._pulse_more)/2
				if self.pulse_more>15:
					self.pulse_more=15
				log.warn('[GPIO - PULSE] доп импульсы: %d среднее: %d'%(self._pulse_more,self.pulse_more))
				self._pulse_more=self.pulse_more
				self.pump_timeout=False
			elif self.pump_timeout and (time.time()-self.pump_timeout)>1.5 and self.pulse_cnt<2:
				if not self.pump_aux and self.pump and not self.pump_paused:
					gp.pump_aux=True


		except Exception, e:
			log.failure('POLL FAILURE')


	def notifyKeyDown(self,keynum):		
		global cur_pulse_start_value
		log.warn('[GPIO] нажата кнопка %d'%keynum)
		self.rpt=False
		if self.pump:
			if 4==keynum:
				if self.pump_paused:
					#cur_pulse_start_value=True
					if not self.pause_ts or (self.pause_ts+2)<time.time():
						self.pause_ts=time.time()
						log.warn('ПРОДОЛЖАЕМ НАЛИВ')
						self.setPumpPause(False)
					else:
						self.pause_ts=time.time()
						log.warn('НЕ ТАК БЫСТРО С ВОЗОБНОВЛЕНИЕМ!')						
				else:
					if self.pulse_cnt>max(pulse_start_value*2,10,self.minpulses):
						if self._wash:
							log.warn('ПРОМЫВКА - ВКЛЮЧАЕМ ПАУЗУ СРАЗУ')
							self.setPumpPause(True)
						elif self.pulses<self.minpulses:
							self.pause_req=self.minpulses
							log.warn('ОТКЛАДЫВАЕМ НАЖАТИЕ ПАУЗЫ %s, уже прошло: %s'%(self.pause_req,self.pulses))
						else:
							if not self.pause_ts or (self.pause_ts+0.5)<time.time():
								self.pause_ts=time.time()
								log.warn('ВКЛЮЧАЕМ ПАУЗУ')
								self.setPumpPause(True)
							else:
								log.warn('НЕ ТАК БЫСТРО С ПАУЗОЙ!')						
				self.nokeydown=keynum
			elif 8==keynum and (self.pump_paused or self._wash):
				self.pause_req=False
				if self._wash:
					log.warn('ПРОМЫВКА - ПРЕКРАЩАЕМ НАЛИВ СРАЗУ')
					self.setPulseCounter(0)
				else:
					"""				
					pp=self.minpulses-self.pulses
					if pp>0:
						log.warn('БУДЕМ ОТКЛАДЫВАТЬ ОКОНЧАНИЕ НАЛИВА')
						if self.pulse_cnt>3:
							self.pulse_cnt=pp if pp>3 else 3
						log.warn('НАЛИВ БУДЕТ ОСТАНОВЛЕН ЧЕРЕЗ: %s'%self.pulse_cnt)
					else:
						log.warn('ПРЕКРАЩАЕМ НАЛИВ')
						self.setPulseCounter(0)
					"""
					log.warn('ПРЕКРАЩАЕМ НАЛИВ')
					self.setPulseCounter(0)
		else:
			self.rpt=[0.7,time.time(),keynum]

		if not self.nokeydown:
			self.factory.send_to_all((u'KEY_DOWN %d'%keynum).encode())
		"""
		try:
			keyboard.press(chr(ord('0')+keynum))
		except:
			keyboard.press(chr(ord('0')+keynum))
		"""
		#try:
		#	keyboard.press_and_release('%s'%chr(ord('0')+keynum))
		#except:
		#	keyboard.press_and_release('%s'%chr(ord('0')+keynum))

	def notifyKeyUp(self,keynum):
		log.info('[GPIO] отжата кнопка %d'%keynum)
		if self.nokeydown!=keynum:
			self.nokeydown=False
			self.factory.send_to_all((u'KEY_UP %d'%keynum).encode())
		self.rpt=False
		"""
		try:
			keyboard.release(chr(ord('0')+keynum))
		except:
			keyboard.release(chr(ord('0')+keynum))
		"""

	def notifyPumpDone(self):
		self.send_mutex.acquire()
		try:
			self.pulse_changed=0
			self.rst_pulse_changed=True
			self.pump_paused=False
		finally:
			self.send_mutex.release()
		_pup=self.pulses if not self.freeze_pulses else self.freeze_pulses
		pup=self.recalc_pulses(_pup)#(self.pulse_more if not self.was_paused else 0))
		log.warn('[GPIO] ЗАДАННЫЙ ОБЬЕМ НАПОЛНЕН испульсов оталиброванных: %s по факту: %s'%(pup,_pup))
		self.factory.send_to_all((u'PUMP OFF %d'%pup).encode())
		self.pulses=0
		self.freeze_pulses=False
		#kiosk.kiosk_logic.getKIOSK().salePollSold(tot)
		#kiosk.kiosk_logic.getKIOSK().saleEnd()

	def notifyPumpTimeout(self):
		log.error('[GPIO] TIMEOUT - НЕ ПОСТУПАЕТ ВОДА')
		#kiosk.kiosk_logic.getKIOSK().queryMode('error_no_water')
		#kiosk.kiosk_logic.getKIOSK().saleEnd()
		self.factory.send_to_all((u'PUMP TIMEOUT %d'%self.recalc_pulses(self.pulses)).encode())
		self.pulses=0
		self.pump_paused=False
		self.removeeventdetect()#GPIO.remove_event_detect(25)

	def notifyBottleSold(self):
		log.warn('[GPIO] ТАРА ПРОДАНА!')
		self.factory.send_to_all((u'BOTTLE SOLD').encode())
		#kiosk.kiosk_logic.getKIOSK().salePollSold(self._bottle_price)		
		#self._bottle_price=0
		#kiosk.kiosk_logic.getKIOSK().saleEnd()

	def notifyBottleNotSold(self):
		log.error('[GPIO] ТАРА НЕ ПРОДАНА!')
		self.factory.send_to_all((u'BOTTLE TIMEOUT').encode())

	def sellBottle(self):
		self.factory.send_to_all((u'TRAY UNLOCKED').encode())
		self.bottle_sold_time=time.time()
		self.mag_bottle=True

	def getPulsePercent(self):
		tot=self.pulse_cnt+self.pulse_passed
		return 100.0*self.pulse_passed/tot if tot else 0

	def getPulseLiter(self):
		return ((self.pulse_passed+self.pulse_more)*12)/1000.0 if self.pulse_passed else 0

	def setPulseCounter(self,count=0):
		"""
		cfg=dict(water=dict(
			flowmeter=dict(resolution=0.012),
			valve=dict(pulses=0),
			correction=dict(enabled=True,permissions=dict(enable_pulses_more=True,enable_fringe=True)),
			fringe_frequency=10.0))
		"""
		if count<=0:
			gp.send_mutex.acquire()
			try:
				self.pause_req=False
				self.pump_done=True
				self.pump=False
				self.was_paused=self.pump_paused
				self.pump_paused=False
				self.pulse_cnt=count
				self.pulse_passed=0
				self.pulse_prev=0
			finally:
				gp.send_mutex.release()

		else:
			_xcount=count
			global pulse_start_value,nlv_pzc
			self.pulse_add_value=0
			nlv_pzc=0
			self.reddis=True
			if count<=0:
				pulse_start_value=0
				self.pulse_coef=1.0
			elif not self.calib:
				self._wash=self.wash
				log.error('УСТАНОВКА СЧЕТЧИКА ИМПУЛЬСОВ: %s'%count)
				coef=0.012/self.cfg['water']['flowmeter']['resolution']
				if 'ml_mul' in self.cfg['water']['flowmeter']:
					mls=self.cfg['water']['flowmeter']['ml_mul']
					mls=int(round(mls/(0.012*coef)))
					if mls!=0:
						count5l=int(round(5.0/(0.012*coef)))
						try:
							new_coef=float(count5l+mls)/count5l
						except:
							new_coef=1.0					
						log.error('СЧЕТЧИК ИМПУЛЬСОВ с учетом ручных корректировок (пропорция): %s'%(count*new_coef))
						coef=coef*new_coef

				_count=int(round(coef*count))
				if 'ml_add' in self.cfg['water']['flowmeter']:
					if _count<(0.5/(0.012*coef)):
						log.warn('Коррекция (добавка) не выполняется, налив малого объема')
					else:
						mls=self.cfg['water']['flowmeter']['ml_add']
						mls=int(round(mls/(0.012*coef)))
						self.pulse_add_value=mls
						_count=_count+mls
						log.error('СЧЕТЧИК ИМПУЛЬСОВ с учетом ручных корректировок (добавка): %s'%_count)
						if _count<1:
							_count=1
				if _count!=count:
					self.pulse_coef=float(count)/float(_count)
					count=_count
					log.error('КОМПЕНСАЦИЯ ПОГРЕШНОСТИ РАСХОДОМЕРА, СЧЕТЧИК ИМПУЛЬСОВ: %s, c=%.03f'%(count,self.pulse_coef))
				else:
					self.pulse_coef=1.0


				if self.cfg['water']['correction']['enabled']:
					if self.cfg['water']['correction']['permissions']['enable_fringe']:
						if count and count>0 and (0==self.fa or self.fa>self.cfg['water']['fringe_frequency']):
							_nc=round(float(count)/83.333)
							count-=int(_nc)
							if count<1:
								count=1
							log.error('ЧАСТОТА %.02f, КОРРКЕЦИЯ СЧЕТЧИКА ИМПУЛЬСОВ: %s'%(self.fa,count))
					if self.cfg['water']['correction']['permissions']['enable_pulses_more']:
						pulse_start_value=self.pulse_more if self.fa>self.cfg['water']['fringe_frequency'] or not self.cfg['water']['correction']['permissions']['enable_fringe'] else int(self.pulse_more/2)
					else:
						pulse_start_value=0							
				else:
					log.error('КОРРЕКТИРОВКИ ОТКЛЮЧЕНЫ!')
					pulse_start_value=0
				pulse_start_value+=self.cfg['water']['valve']['pulses']
			else:
				log.error('НАЛИВ В РЕЖИМЕ КАЛИБРОВКИ: %s'%count)
				pulse_start_value=0
				self.pulse_coef=1.0

			if count<10 or count<(pulse_start_value*2):
				log.warn('[GPIO] К величайшему сожалению клиент отправляется на йух, импульсов слишком мало: %s'%count);
				if _xcount>0:
					self.factory.send_to_all((u'PUMP OFF %d'%_xcount).encode())
				count=0

			if self.disabled:
				log.error('HW DRIVER DISABLED!!!!!!!!!!!!!!!!!!!!!!!')
				self.notifyPumpTimeout()
				return False
			else:
				gp.send_mutex.acquire()
				try:
					self.pause_req=False
					if count and count>0:
						global cur_pulse_start_value
						cur_pulse_start_value=True
						self.removeeventdetect()#GPIO.remove_event_detect(22)
						self.addeventdetect() #GPIO.add_event_detect(22, GPIO.BOTH, callback=pulse_irq, bouncetime=10)
						self.freeze_pulses=False
						self.pulses=0
						#count-=self.pulse_more
						if count<(self.pulse_more+1): count=(self.pulse_more+1)
						self.pump_timeout=time.time()
						self.pump_done=False
						self.pump=True
						self.was_paused=False
						self.update_outputs()
					else:
						self.pump_done=True
						self.pump=False
						self.was_paused=self.pump_paused
					self.pump_paused=False
					self.pulse_cnt=count
					self.pulse_passed=0
					self.pulse_prev=0
				finally:
					gp.send_mutex.release()
			return True

	def setPumpPause(self,aPaused):
		gp.send_mutex.acquire()
		try:
			if not self.pump:
				self.removeeventdetect()#GPIO.remove_event_detect(22)
				self.addeventdetect() #GPIO.add_event_detect(22, GPIO.BOTH, callback=pulse_irq, bouncetime=10)					
			if aPaused and self.pump and self.pulse_cnt>10:
				self.pump_timeout=time.time()
				if not self.pump_paused:
					self.factory.send_to_all((u'PUMP PAUSED %d'%self.recalc_pulses(self.pulses if not self.freeze_pulses else self.freeze_pulses)).encode())
				self.pump_paused=True
			else:
				global nlv_pzc
				nlv_pzc+=1				
				if nlv_pzc<3:
					if self.pump_paused:
						if not ('pause_add' in self.cfg['water']):
							self.cfg['water']['pause_add']=5
						self.pulse_cnt+=self.cfg['water']['pause_add']
				self.pump_timeout=time.time()
				self.freeze_pulses=False
				self.pump_paused=False
		finally:
			gp.send_mutex.release()

	def getPulseCounter(self):
		return self.pulse_cnt

	def setDoorLock(self,locked=False):
		if locked:
			self.door_unlock_time=False
			self.door_unlock=False
		else:
			self.door_unlock_time=time.time()
			self.door_unlock=True
		self.update_outputs()

	def setMinPulses(self,p):
		self.minpulses=p

	def getLogger(self):
		return log


