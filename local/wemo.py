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


last_power = 0

while True:
	power = switch.current_power
	print "power is " + str(power)
	if power < 4500 and last_power > 4500:
		notify_AWS(OFF)
		last_state = "off"
	elif power > 100 and last_power < 100:
		notify_AWS(ON)
		last_state = "on"
	time.sleep(2)


