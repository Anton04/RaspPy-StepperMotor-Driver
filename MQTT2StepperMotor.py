#!/usr/bin/python

# Author: Anton Gustafsson
# Released under MIT license 




from StepperMotorDriver import MotorControl
import mosquitto
from uuid import getnode as get_mac
import sys



class MQTTMotorControl(mosquitto.Mosquitto,MotorControl):
  
	def __init__(self,Pins = [24,25,8,7],ip = "localhost", port = 1883, clientId = "MQTT2StepperMotor", user = "driver", password = "1234", prefix = "StepperMotor"):
		mosquitto.Mosquitto.__init__(self,clientId)
		
		MotorControl.__init__(self,Pins)
    
    		#Get mac adress. 
    		mac = get_mac()
    
    		#Make a number based on pins used.
    		pinid = ""
    		for pin in Pins:
      			pinid += "%02i" % pin
    
    		self.prefix = prefix + "/" + str(mac) + "/" + pinid
		self.ip = ip
    		self.port = port
    		self.clientId = clientId
		self.user = user
    		self.password = password
    		
    		if user != None:
    			self.username_pw_set(user,password)

		#self.will_set( topic =  "system/" + self.prefix, payload="Offline", qos=1, retain=True)
		self.will_set( topic =  self.prefix, payload="Offline", qos=1, retain=True)
		print "Connecting to:" +ip
    		self.connect(ip,keepalive=10)
    		self.subscribe(self.prefix + "/#", 0)
    		self.on_connect = self.mqtt_on_connect
    		self.on_message = self.mqtt_on_message
    		#self.publish(topic = "system/"+ self.prefix, payload="Online", qos=1, retain=True)
    		self.publish(topic = self.prefix, payload="Online", qos=1, retain=True)
    
    
    		#mosquitto.Mosquitto.loop_start(self)
    
	def mqtt_on_connect(self, selfX,mosq, result):
    		print "MQTT connected!"
    		self.subscribe(self.prefix + "/#", 0)
    		
    	def mqtt_on_message(self, selfX,mosq, msg):
    		print("RECIEVED MQTT MESSAGE: "+msg.topic + " " + str(msg.payload))
    		
    		topics = msg.topic.split("/")
    		
    		try:    		

	    		if len(topics[-1]) == 0:
	    			topics = topics[:-1]

			cmd = topics[-1].lower()
	    		
	    		if cmd == "speed":
	    			self.speed = int(msg.payload)
	    		elif cmd == "step":
	    			self.StepN(int(msg.payload))
	    		elif cmd == "moveto":
	    			self.MoveTo(int(msg.payload))
	    		elif cmd == "calibrate":
	    			self.calibrate()
	    			
	    	except Exception,e: print str(e)
    		
    		return

if __name__ == "__main__":


	if len(sys.argv) == 2:
		ip = sys.argv[1]
	else:
		ip = "localhost"
		
	print ip

	m = MQTTMotorControl(ip = ip)
	
	m.slack = 41
	m.loop_forever()

