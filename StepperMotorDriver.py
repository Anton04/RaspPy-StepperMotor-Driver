import time
import RPi.GPIO as GPIO


class MotorControl:
	def __init__(self,Pins = [24,25,8,7]):
		GPIO.setmode(GPIO.BCM)
		self.StepPins = Pins
		self.Counter = 0
		self.Setup()
		
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
		return


if __name__ == "__main__":

	m = MotorControl()
	#m.StepN(100,20)
	while(1):
		f=input('Please enter a value:')
		m.StepN(f,20)


	

		
	
