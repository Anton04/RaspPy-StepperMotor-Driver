# Author: Anton Gustafsson
# Released under MIT license 

#!/usr/bin/python



from StepperMotorDriver import MotorControl
import mosquitto
from uuid import getnode as get_mac



class MQTTMotorControl(mosquitto.Mosquitto,MotorControl):
  
  def __init__(self,Pins = [24,25,8,7],ip = "localhost", port = 1883, clientId = "MQTT2StepperMotor", user = "driver", password = "1234", prefix = "StepperMotor"):
    mosquitto.Mosquitto.__init__(self,clientId)
    
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

		self.will_set( topic =  "system/" + self.prefix, payload="Offline", qos=1, retain=True)
		self.will_set( topic =  self.prefix, payload="Offline", qos=1, retain=True)
    print "Connecting"
    self.connect(ip,keepalive=10)
    self.subscribe(self.prefix + "/#", 0)
    self.on_connect = self.mqtt_on_connect
    self.on_message = self.mqtt_on_message
    self.publish(topic = "system/"+ self.prefix, payload="Online", qos=1, retain=True)
    self.publish(topic = self.prefix, payload="Online", qos=1, retain=True)
    		
    		

		#thread.start_new_thread(self.ControlLoop,())	
		self.loop_start()


if __name__ == "__main__":

	m = MQTTMotorControl()

