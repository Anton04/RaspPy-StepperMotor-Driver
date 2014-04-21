#!/usr/bin/python

import time
import RPi.GPIO as GPIO


class MotorControl:
	def __init__(self,Pins = [24,25,8,7]):
		GPIO.setmode(GPIO.BCM)
		self.StepPins = Pins
		self.Counter = 0
		self.Setup()
		
		self.moves_since_calibration = None
		self.hasstop = True
		self.abs_pos = -1
		
	def Setup(self):
		for pin in self.StepPins:
  			print "Setup pins"
	  		GPIO.setup(pin,GPIO.OUT)
	  		GPIO.output(pin, False)

	def Shutdown(self):
	        for pin in self.StepPins:
	                GPIO.output(pin, False)
		return

	def Step(self,ForwardDirection = True):
		if self.Counter == 0:
			GPIO.output(self.StepPins[0], ForwardDirection)
		elif self.Counter == 1:
			GPIO.output(self.StepPins[3], not ForwardDirection)
		elif self.Counter == 2:
	                GPIO.output(self.StepPins[1], ForwardDirection)
        	elif self.Counter == 3:
	                GPIO.output(self.StepPins[0], not ForwardDirection)
		elif self.Counter == 4:
	                GPIO.output(self.StepPins[2], ForwardDirection)
	        elif self.Counter == 5:
	                GPIO.output(self.StepPins[1], not ForwardDirection)
		elif self.Counter == 6:
	                GPIO.output(self.StepPins[3], ForwardDirection)
	        elif self.Counter == 7:
	                GPIO.output(self.StepPins[2], not ForwardDirection)

		if ForwardDirection:
			self.Counter += 1
		else:
			self.Counter -= 1

		if self.Counter > 7:
			self.Counter = 0
		elif self.Counter < 0:
			self.Counter = 7

		return self.Counter

	def StepN(self,N,speed):

		move = N

		if (N>0):
			dir = True
		else:	
			dir = False
			N = N * -1
	
		for f in range(0,N):
			self.Step(dir)

			stime = 20 * (f+1)
			
			if stime > speed:
				stime = speed

			time.sleep(1.0/stime)
		self.Shutdown()
		
		self.abs_pos += move
		if self.moves_since_calibration != None:
			self.moves_since_calibration += 1
		
		return

	#This function assumes that you have a stop that makes it impossible for the engine to turn more than to a certain point. 
	#It then uses it for calibrating to an known absolute position. 
	def CalibrateAgainstStop(self):
		if self.moves_since_calibration == None:
			self.StepN(-3000,200)
		else:
			self.StepN(-1*(100+self.abs_pos),50)
		self.abs_pos = 0
		self.moves_since_calibration = 0
		
	def Calibrate(self):
		print "Calibring"
		if self.hasstop:
			self.CalibrateAgainstStop()
		#TODO implement calibratino against I/O connected sensor 
		print "Done!"	
		
	#Moves to an abosulte position	
	def MoveTo(self,pos,speed = 20,auto_recalib = False):
		if self.moves_since_calibration == None:
			self.Calibrate()
	
		if auto_recalib and moves_since_calib > 1000:
			self.Calibrate()
		
		delta = pos - self.abs_pos

		print "Current position is: %i  Moving %i steps to %i" %(self.abs_pos,delta,pos)
	
		self.StepN(delta,speed)
	
		return

if __name__ == "__main__":

	m = MotorControl()
	#m.StepN(100,20)
	while(1):
		f=input('Please enter a value:')
		m.MoveTo(f,100)


	

		
	
