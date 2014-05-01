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
		self.visual_pos = -1
		
		self.slack = 0
		self.slackIndex = self.slack/2
		
		self.speed = 100
		
		self.lastdir = True
		
	def Setup(self):
		for pin in self.StepPins:
  			print "Setup pins"
	  		GPIO.setup(pin,GPIO.OUT)
	  		GPIO.output(pin, False)

	def Shutdown(self):
	        for pin in self.StepPins:
	                GPIO.output(pin, False)
		return
	
		
	
	def DoubleStep(self,ForwardDirection=True):
	
	     	if ForwardDirection:
			if self.lastdir == ForwardDirection:
				self.Counter += 1
			if not self.slackIndex >= self.slack:
				self.slackIndex += 1
		else:
			if self.lastdir == ForwardDirection:
				self.Counter -= 1
			if not self.slackIndex <= 0:
				self.slackIndex -= 1
				
		self.lastdir = ForwardDirection

		if self.Counter > 7:
			self.Counter = 0
		elif self.Counter < 0:
			self.Counter = 7
	
		#Transitions		
		if self.Counter == 0:
			GPIO.output(self.StepPins[0], ForwardDirection)
			GPIO.output(self.StepPins[3], not ForwardDirection)
		elif self.Counter == 2:
	                GPIO.output(self.StepPins[1], ForwardDirection)
	                GPIO.output(self.StepPins[0], not ForwardDirection)
		elif self.Counter == 4:
	                GPIO.output(self.StepPins[2], ForwardDirection)
	                GPIO.output(self.StepPins[1], not ForwardDirection)
		elif self.Counter == 6:
	                GPIO.output(self.StepPins[3], ForwardDirection)
	                GPIO.output(self.StepPins[2], not ForwardDirection)
			
		return self.Counter

	def Step(self,ForwardDirection = True):

		if ForwardDirection:
			if self.lastdir == ForwardDirection:
				self.Counter += 1
			if not self.slackIndex >= self.slack:
				self.slackIndex += 1
		else:
			if self.lastdir == ForwardDirection:
				self.Counter -= 1
			if not self.slackIndex <= 0:
				self.slackIndex -= 1
				
		self.lastdir = ForwardDirection

		if self.Counter > 7:
			self.Counter = 0
		elif self.Counter < 0:
			self.Counter = 7

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

		return self.Counter

	def StepN(self,N,speed=None,Double = False):
		
		if N == 0:
			return 0
		
		if speed == None:
			speed = self.speed

		move = N

		if (N>0):
			dir = True
			slack = self.slack - self.slackIndex
		else:	
			dir = False
			N = N * -1
			slack = self.slackIndex
	
		for f in range(0,N + slack):
			
			stime = 20 * (f+1)
			
			if stime > speed:
				stime = speed

			time.sleep(1.0/stime)
			
			if Double:
				self.DoubleStep(dir)
			else:
				self.Step(dir)

			
			
		#This saves power but destroys the calibration after some movement. 	
		#self.Shutdown()
		
		#Calculate slack from gearbox. 
	#	self.slackIndex += move
	#	if self.slackIndex < 0:
	#		self.slackIndex = 0
	#	elif self.slackIndex > self.slack:
	#		self.slackIndex = self.slack
		
		if dir:
			movement = N + slack
		else:
			movement = -1* (N+slack)
			
		self.visual_pos += move
		self.abs_pos += movement
		
		if self.moves_since_calibration != None:
			self.moves_since_calibration += 1
		
		return movement

	#This function assumes that you have a stop that makes it impossible for the engine to turn more than to a certain point. 
	#It then uses it for calibrating to an known absolute position. 
	def CalibrateAgainstStop(self):
		if self.moves_since_calibration == None:
			self.StepN(-3000,1600)
		else:
			self.StepN(-1*(100+self.abs_pos),50,True)
		self.abs_pos = -4
		self.visual_pos = -4
		self.moves_since_calibration = 0
		self.slackIndex = 0
		
	def Calibrate(self):
		print "Calibring"
		if self.hasstop:
			self.CalibrateAgainstStop()
		#TODO implement calibratino against I/O connected sensor 
		print "Done!"	
		
	#Moves to an abosulte position	
	def MoveTo(self,pos,speed = None,auto_recalib = False):
		if self.moves_since_calibration == None:
			self.Calibrate()
	
		if auto_recalib and moves_since_calib > 1000:
			self.Calibrate()
		
		delta = pos - self.visual_pos

		print "  Visual position is: %i  Moving %i steps to %i" %(self.visual_pos,delta,pos)
		print "Absolute position is: %i  SlackIndex: %i" %(self.abs_pos,self.slackIndex)
	
		movement = self.StepN(delta,speed,True)
	
		print "Actual movement: %i" % movement
	
		return

if __name__ == "__main__":

	m = MotorControl()
	m.slack = 41
	#m.StepN(100,20)
	while(1):
		f=raw_input('Please enter a value:')
		
		if str(f) == "Test":
			for f in range(0,20):
				m.MoveTo(300,400)
				m.MoveTo(800,400)
		else:		
			m.MoveTo(int(f),100)


	

		
	
