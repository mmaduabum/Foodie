from ouimeaux.environment import Environment
import time
import httplib

ON = "on"
OFF = "off"

def on_switch(switch):
    print "Switch found!", switch.name

def on_motion(motion):
    print "Motion found!", motion.name

env = Environment(on_switch, on_motion)
env.start()

#env.list_switches()

switch = env.get_switch('ymcmb')


def notify_AWS(state):
	conn = httplib.HTTPConnection("52.39.99.178")
	msg = "RAMYour device is now " + state
	conn.request("POST", "", msg)


last_state = "off"

while True:
	power = switch.current_power
	print "power is " + str(power)
	if power < 10 and last_state == "on":
		notify_AWS(OFF)
		last_state = "off"
	elif power > 2000 and last_state == "off":
		notify_AWS(ON)
		last_state = "on"
	time.sleep(2)


