from ouimeaux.environment import Environment
import time
import httplib

ON = "on"
OFF = "off"
THRESH = 400


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
	if state == OFF:
		msg = "RAMYour device is now " + state + ". To unfollow, reply 'unfollow'" 
	else:
		msg = "RAMYour device is now " + state
	conn.request("POST", "", msg)


def powering_off(history):
	old, med, new = history
	return old > med and med > new

def powering_on(history):
	old, med, new = history
	return old < med and med < new

last_state = "off"
last_powers = [0, 0, 0]

while True:
	power = switch.current_power
	last_powers.pop(0)
	last_powers.append(power)
	print "power is " + str(power)
	if power < THRESH and powering_off(last_powers) and last_state == "on":
		notify_AWS(OFF)
		last_state = "off"
	elif power < THRESH and powering_on(last_powers) and last_state == "off":
		notify_AWS(ON)
		last_state = "on"
	time.sleep(1)


