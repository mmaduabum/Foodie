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


def powering_off(history):
	old, med, new = history
	return old > med and med > new

def powering_on(history):
	old, med, new = history
	return old < med and med < new


last_powers = [0, 0, 0]

while True:
	power = switch.current_power
	l.pop(0)
	l.append(power)
	print "power is " + str(power)
	if power < 4500 and last_power powering_off(last_powers):
		notify_AWS(OFF)
		last_state = "off"
	elif powering_on(last_powers):
		notify_AWS(ON)
		last_state = "on"
	time.sleep(2)


