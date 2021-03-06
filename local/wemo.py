from ouimeaux.environment import Environment
import time
import httplib
import json
import sys

ON = 1
OFF = 0
THRESH = "threshold"
MIN = "min"
YMCMB_THRESH = 36000
YMCMB_MIN = 650
PADDY_THRESH = 1400000
HUB_PORT_NUMBER = 3758
NAME = "name"
SWITCH = "switch"
STATE = "state"
YMCMB_ID = 1
PADDY_ID = 2
ID = "ID"

def on_switch(switch):
    print "Switch found!", switch.name

def on_motion(motion):
    print "Motion found!", motion.name



def notify_AWS(switches):
	print "State change detected. Sending HTTP"
	msg = {}
	for s in switches:
		msg[s[ID]] = s[STATE]
	data = json.dumps(msg)
	conn = httplib.HTTPConnection("52.39.99.178", HUB_PORT_NUMBER)
	conn.request("POST", "", data)


def powering_off(history):
	old, med, new = history
	return old > med and med > new

def powering_on(history):
	old, med, new = history
	return old < med and med < new


def run_local_server(switches):
	#send initial state info to AWS
	notify_AWS(switches)

	num_switches = len(switches)
	print str(num_switches) + " Found!"

	last_powers_list = [[0, 0, 0]]*num_switches
	for i in range(num_switches): last_powers_list[i] = [0, 0, 0]
	last_states_list = [OFF]*num_switches
	#check power statuses forever	
	while True:
		change = False
		for i, (s, last_state, last_powers) in enumerate(zip(switches, last_states_list, last_powers_list)):
			power = s[SWITCH].current_power
			last_powers_list[i].pop(0)
			last_powers_list[i].append(power)
			if power < s[THRESH] and power >= s[MIN] and powering_off(last_powers) and last_state == ON:
				change = True
				last_states_list[i] = OFF
				switches[i][STATE] = OFF
			elif power < s[THRESH] and power >= s[MIN] and powering_on(last_powers) and last_state == OFF:
				change = True
				last_states_list[i] = ON
				switches[i][STATE] = ON
		#if any state has changed, notify AWS
		if change:
			change = False
			notify_AWS(switches)
		#wait for next power readout to be available
		time.sleep(1)


def go_pi():
	try:
		sys.stderr = open("otherlog.txt", "wa+")
		sys.stdout = open("log.txt", "wa+")
		print "Powering up server..."
		switches = []
		env = Environment(on_switch, on_motion)
		env.start()
		#search until a switch is found
		tries = 0
		print "Searching for switches..."
		while True:
			tries += 1
			names = env.list_switches()
			if len(names) > 0: break
			if tries == 100: 
				print "FAILED to find a switch after 100 tries"
				sys.exit()
		#create a dictionary object wrapper for each found switch
		for switch_name in names:
			s = {NAME : switch_name, SWITCH : None, STATE : OFF, ID : None, THRESH : None, MIN : 0}
			if switch_name == "ymcmb":
				ymcmb = env.get_switch('ymcmb')
				s[SWITCH] = ymcmb
				s[ID] = YMCMB_ID
				s[THRESH] = YMCMB_THRESH
				s[MIN] = YMCMB_MIN
			elif switch_name == "patty":
				paddy = env.get_switch('patty')
				s[SWITCH] = paddy
				s[ID] = PADDY_ID
				s[THRESH] = PADDY_THRESH
			#create a list of all found switches
			switches.append(s)

		run_local_server(switches)
	except:
		pass


if __name__ == "__main__":
	while True: go_pi()
